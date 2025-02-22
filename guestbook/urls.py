from django.urls import path

from . import views

app_name = "guestbook"
urlpatterns = [
    # Index view.
    path("", views.index, name="index"),
    # Dashboard view.
    path("dashboard/", views.dashboard, name="dashboard"),
    # Join view.
    path("join/", views.join, name="join"),
    # Join view with join code URL parameter.
    path("join/<str:join_code>/", views.join, name="join_with_code"),
    # JSON endpoint for join code.
    path("refresh-code/", views.get_join_code, name="refresh_code"),
    # HTML partial to update visitors section on dashboard.
    path("visitors-partial/", views.get_visitors_partial, name="visitors_partial"),
    # JSON endpoint for random name generation.
    path("name/", views.get_name, name="name"),
]
