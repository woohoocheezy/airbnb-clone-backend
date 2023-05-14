from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from .serializers import PrivateUserSerializer


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
