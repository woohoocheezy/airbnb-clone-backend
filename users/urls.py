from django.urls import path
from .views import (
    Me,
    Users,
    PublicUser,
    UserReviews,
    HostRooms,
    ChangePassword,
    LogIn,
    LogOut,
)

urlpatterns = [
    path("", Users.as_view()),
    path("me", Me.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
    path("@<str:username>", PublicUser.as_view()),
    path("@<str:username>/reviews", UserReviews.as_view()),
    path("@<str:username>/rooms", HostRooms.as_view()),
]
