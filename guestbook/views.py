from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta
from django.db import connection

from .models import Visit, Visitor, AvatarImage


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


def avatars():
    return AvatarImage.objects.all()[:12]


def base_context():
    # TODO: make location name dynamic.
    location = "CalsZone"
    return {"location": location, "avatars": avatars()}


def dashboard(request):
    # TODO: make dynamic.
    join_code = "XHQNZS"
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


def index(request, visitor_id: int = None):
    # TODO: if visitor visited since midnight today, show page with stats.
    # TODO: otherwise, redirect to join? Or maybe just show a prominent join button?
    context = base_context()

    if visitor_id:
        visitor = Visitor.objects.get(id=visitor_id)
        context["visitor"] = visitor

    return render(request, "guestbook/index.html", context=context)


def join(request, join_code: str = None, visitor_id: int = None):
    if request.method == "POST":
        # Handle POST.
        data = request.POST
        code = data.get("code")
        name = data.get("name")
        avatar_url = data.get("avatar_url")
        # Check join code against current code for current timestep and next timestep.

        # Create and persist visitor.
        visitor = Visitor(name=name, avatar_url=avatar_url)
        visitor.save()
        # TODO: maybe render the template directly from this view?
        return redirect("guestbook:stats", visitor_id=visitor.id)
    else:
        # Handle GET.
        context = base_context()
        if join_code:
            context["join_code"] = join_code
        if visitor_id:
            context["visitor"] = Visitor.objects.get(id=visitor_id)
        return render(request, "guestbook/join.html", context=context)
