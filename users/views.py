from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from reviews.models import Review
from reviews.paginations import ReviewPagination
from reviews.serializers import ReviewSerializer
from rooms.models import Room
from rooms.paginations import HostRoomPagination
from rooms.serializers import HostRoomSerializer
from .serializers import PrivateUserSerializer, PublicUserSerializer
from .models import User


class Me(APIView):

    """APIView for 'GET/PUT /me' request handler"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """'GET /me' handler to display user's private profile data

        Keyword arguments:
        request -- the request from user
        Return: the user own data except password
        """

        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        """'PUT /me' handler to change user data from user's private profile data

        Keyword arguments:
        request -- the request from user
        Return: the 'changed' user own data except password
        """

        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class Users(APIView):

    """APIView for 'POST  /users' request handler"""

    def post(self, request):
        """POST /users' handler to create a user

        Keyword arguments:
        request -- the request from user
        Return: the created user
        """

        # password validation
        password = request.data.get("password")
        if not password:
            raise ParseError

        serializer = PrivateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()

            serializer = PrivateUserSerializer(user)

            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    """APIView for 'GET /users/@<username>' request handler"""

    def get(self, request, username):
        """GET /users/@<username>' handler to display a user

        Keyword arguments:
        request -- the request from user
        username -- the username to display
        Return: the user with username
        """
        try:
            user = User.objects.get(username=username)
        except:
            raise NotFound
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


class UserReviews(generics.ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    def get_queryset(self):
        username = self.kwargs.get("username")
        if User.objects.filter(username=username).exists():
            queryset = (
                Review.objects.filter(user__username=username)
                .all()
                .order_by("-created_at")
            )
            return queryset
        else:
            raise ParseError(f"No user with that nickname({username}) exists.")


class HostRooms(generics.ListAPIView):
    serializer_class = HostRoomSerializer
    pagination_class = HostRoomPagination

    def get_queryset(self):
        username = self.kwargs.get("username")
        if User.objects.filter(username=username).exists():
            queryset = Room.objects.filter(owner__username=username).order_by(
                "-created_at"
            )
            return queryset
        else:
            raise ParseError(f"No user with that nickname({username}) exists.")


class ChangePassword(APIView):
    """APIView for 'PUT /users/change-password' request handler"""

    permission_classes = [IsAuthenticated]

    def put(self, reqeust):
        """PUT request handler for changing user's password

        Keyword arguments:
        request -- the request from user
        Return: status code('HTTP_200_OK' for if case & HTTP_400_BAD_REQUEST' for else case)
        """

        user = reqeust.user
        old_password = reqeust.data.get("old_password")
        new_password = reqeust.data.get("new_password")

        if not old_password or not new_password:
            raise ParseError

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):

    """APIView for 'POST /users/log-in' request handler for user to log in"""

    def post(self, request):
        """POST request handler for user to log in

        Keyword arguments:
        request -- the request from user
        Return: response messages
        """

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})

        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):

    """APIView for 'POST /users/log-out' request handler for user to log out"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """POST request handler for user to log out

        Keyword arguments:
        request -- the request from user
        Return: response messages
        """

        logout(request)
        return Response({"ok": "Bye!"})
