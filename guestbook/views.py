from django.shortcuts import render
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


def join(request):
    return render(request, "guestbook/join.html", context=base_context())


def join_with_code(request, join_code: str):
    context = {"code": join_code}
    return render(request, "guestbook/join.html", context=base_context())
