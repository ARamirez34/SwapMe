from django.urls import path
from .views import login_view, logout_view, success_view, edit_profile

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("success/", success_view, name="success"),
    path("edit-profile/", edit_profile, name="edit_profile"),
]
