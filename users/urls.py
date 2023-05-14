from django.urls import path
from .views import Me, Users, PublicUser

urlpatterns = [
    path("", Users.as_view()),
    path("me", Me.as_view()),
]
