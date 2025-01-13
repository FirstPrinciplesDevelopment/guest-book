from django.urls import path

from . import views

app_name = "guestbook"
urlpatterns = [
    # Index view.
    path("", views.index, name="index"),
    # Stats view.
    path("stats/<int:visitor_id>/", views.index, name="stats"),
    # Dashboard view.
    path("dashboard/", views.dashboard, name="dashboard"),
    # Join view.
    path("join/", views.join, name="join"),
    # Join view with join code URL parameter.
    path("join/<str:join_code>/", views.join, name="join_with_code"),
    path("refresh-code/", views.get_join_code, name="refresh_code"),
]
