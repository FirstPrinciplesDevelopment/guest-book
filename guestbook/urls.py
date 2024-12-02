from django.urls import path

from . import views

app_name = "guestbook"
urlpatterns = [
    # Dashboard view.
    path("dashboard/", views.dashboard, name="dashboard"),
    # Join view.
    path("join/", views.join, name="join"),
    # Join view with join code URL parameter.
    path("join/<str:join_code>/", views.join_with_code, name="join_with_code"),
]
