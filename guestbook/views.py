from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta
from django.db import connection
from django.conf import settings

from guestbook.services.visitors_service import (
    generate_name,
    validate_name,
    random_avatars,
)

from .models import Visit, Visitor, AvatarImage
from .totp import totp, totp_offset

import logging
import time
import json

logger = logging.getLogger(__name__)


def build_notification(status: str, message: str) -> dict:
    return {"type": status, "message": message}


def midnight_today():
    midnight_today = timezone.localtime().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return midnight_today


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def visitors_since(datetime):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT DISTINCT "guestbook_visitor"."id",
                                "guestbook_visitor"."name",
                                "guestbook_visitor"."avatar_url"
                            FROM "guestbook_visitor"
                            INNER JOIN "guestbook_visit"
                                ON ("guestbook_visitor"."id" = "guestbook_visit"."visitor_id")
                            WHERE "guestbook_visit"."visit_datetime" >= %s
                            ORDER BY "guestbook_visitor"."name" DESC""",
            [datetime],
        )
        return dictfetchall(cursor=cursor)


def get_current_totp():
    return totp(settings.TOTP_SECRET, settings.TOTP_TIMESTEP)


def get_previous_totp():
    return totp_offset(
        settings.TOTP_SECRET, settings.TOTP_TIMESTEP, settings.TOTP_TIMESTEP
    )


def get_join_url():
    return f"{settings.BASE_URL}/join/"


def get_time_step():
    return settings.TOTP_TIMESTEP


def seconds_remaining(time_step: int = 30, offset: int = 0) -> int:
    """Given a timestep and offset, calculate how many seconds until the TOTP will change."""
    seconds_elapsed = int((time.time() + offset) % time_step)
    return time_step - seconds_elapsed


def base_context():
    # TODO: make location name dynamic.
    location = "CalsZone"
    return {"location": location, "avatars": random_avatars()}


def dashboard(request):
    join_code = get_current_totp()
    todays_visitors = visitors_since(midnight_today())
    weeks_visitors = visitors_since(midnight_today() - timedelta(days=7))
    months_visitors = visitors_since(midnight_today() - timedelta(days=30))

    return render(
        request,
        "guestbook/dashboard.html",
        {
            "join_code": join_code,
            "visitors": {
                "today": todays_visitors,
                "week": weeks_visitors,
                "month": months_visitors,
            },
            **base_context(),
        },
    )


def index(request, notifications: dict = None):
    # TODO: if visitor visited since midnight today, show page with stats.
    # TODO: otherwise, redirect to join? Or maybe just show a prominent join button?
    context = {
        "notifications": notifications,
        **base_context(),
    }

    return render(request, "guestbook/index.html", context=context)


def join(request, join_code: str = None, visitor_id: int = None):
    if request.method == "POST":
        # Handle POST.
        data = request.POST
        code = data.get("code")
        name = data.get("name")
        avatar_url = data.get("avatar_url")
        # Check join code against current code for current timestep and next timestep.
        if code == get_current_totp() or code == get_previous_totp():
            # Validate name.
            if validate_name(name):
                # Create and persist visitor.
                visitor = Visitor(name=name, avatar_url=avatar_url)
                visitor.save()
                # Create and persist visit.
                visit = Visit(visitor=visitor)
                visit.save()
                # Redirect to the index page with a welcome notification.
                context = {
                    "notifications": [
                        build_notification("success", "Thanks for visiting!")
                    ],
                    **base_context(),
                }
                return render(request, "guestbook/index.html", context=context)
            else:
                context = {
                    "notifications": [build_notification("error", "Invalid name.")],
                    **base_context(),
                }
                return render(request, "guestbook/join.html", context=context)
        else:
            # Invalid code.
            context = {
                "notifications": [build_notification("error", "Invalid join code.")],
                **base_context(),
            }
            if visitor_id:
                context["visitor"] = Visitor.objects.get(id=visitor_id)
            return render(request, "guestbook/join.html", context=context)
    else:
        # Handle GET.
        context = base_context()
        if join_code:
            context["join_code"] = join_code
        if visitor_id:
            context["visitor"] = Visitor.objects.get(id=visitor_id)
        return render(request, "guestbook/join.html", context=context)


def get_join_code(request):
    if request.user.is_superuser and request.user.is_active:
        data = {
            "code": get_current_totp(),
            "step": get_time_step(),
            "remaining": seconds_remaining(),
            "url": get_join_url(),
        }
        json_str = json.dumps(data)
        return HttpResponse(json_str, content_type="application/json")
    elif request.user.is_authenticated:
        return HttpResponse("Forbidden", status=403)
    else:
        return HttpResponse("Unauthorized", status=401)


def get_visitors_partial(request):
    if request.user.is_superuser and request.user.is_active:
        todays_visitors = visitors_since(midnight_today())
        weeks_visitors = visitors_since(midnight_today() - timedelta(days=7))
        months_visitors = visitors_since(midnight_today() - timedelta(days=30))
        return render(
            request,
            "guestbook/visitors.partial.html",
            {
                "visitors": {
                    "today": todays_visitors,
                    "week": weeks_visitors,
                    "month": months_visitors,
                },
                **base_context(),
            },
        )
    elif request.user.is_authenticated:
        return HttpResponse("Forbidden", status=403)
    else:
        return HttpResponse("Unauthorized", status=401)


def get_name(request):
    data = {"name": generate_name()}
    json_str = json.dumps(data)
    return HttpResponse(json_str, content_type="application/json")
