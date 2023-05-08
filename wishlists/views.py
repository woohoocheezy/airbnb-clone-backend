from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_200_OK
from rooms.models import Room
from .models import Wishlist
from .serializers import WishlistSeralizer


class Wishlists(APIView):
    """the APIView for wishlist"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """GET /wishilists
            Displaying all 'wishlists' that a user created

        Keyword arguments:
        self --
        request --
        Return: the response with the data of wishlist serializer
        """

        all_wishilists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSeralizer(
            all_wishilists,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    def post(self, request):
        """POST /wishilists
           create a 'wishlist' of a user

        Keyword arguments:
        self --
        request --
        Return: the response with the data of wishlist serializer if the serializer is valid or the error
        """
        serializer = WishlistSeralizer(data=request.data)

        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            serializer = WishlistSeralizer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):
    """The API view of the detail information of 'Wishlist'
       Handling requests for 'GET/PUT/DELETE /wishlists/{ID of a wishlist}'
       ex) GET /wishlists/1

    Keyword arguments:
    None
    Return: None
    """

    # a user can only access its own wishlist
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        """returning the object of a wishlist making a query by checking pk and user

        Keyword arguments:
        pk -- the pk of the wishlist
        user -- the user of the wishlist is same as the user who requests
        Return: the wishlist object of a request.user with the wishlist's pk, or NotFound
        """

        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        """handling the request about 'GET /wishlists/{ID of a wishlist}'

        Keyword arguments:
        request -- the request that a user make
        pk -- the primary key or the requested wishlist
        Return: the serialized data of the wishlist with 'the pk & the user'
        """

        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSeralizer(wishlist, context={"request": request})

        return Response(serializer.data)

    def delete(self, request, pk):
        """handling the request about 'DELETE /wishlists/{ID of a wishlist}'

        Keyword arguments:
        request -- the request that a user make
        pk -- the primary key or the requested wishlist
        Return: HTTP_200_OK
        """

        wishlist = self.get_object(pk, request.user)
        wishlist.delete()

        return Response(status=HTTP_200_OK)

    def put(self, request, pk):
        """handling the request about 'PUT /wishlists/{ID of a wishlist}'

        Keyword arguments:
        request -- the request that a user make
        pk -- the primary key or the requested wishlist
        Return: the serialized data of the wishlist with 'the pk & the user' which is UPDATED
        """

        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSeralizer(wishlist, data=request.data, partial=True)

        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSeralizer(wishlist)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class WishlistToogle(APIView):

    """The API view for adding/removing a room/experience to/from the wishlist
       Handling requests for 'PUT /wishlists/{ID of a wishlist}/rooms/{ID of a room}'
       ex) PUT /wishlists/1/rooms/1

    Keyword arguments:
    None
    Return: None
    """

    def get_wishlist(self, pk, user):
        """returning the object of a wishlist making a query by checking pk and user

        Keyword arguments:
        pk -- the pk of the wishlist
        user -- the user of the wishlist is same as the user who requests
        Return: the Wishlist object of a request.user with the wishlist's pk, or NotFound
        """

        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        """returning the object of a room making a query by checking pk

        Keyword arguments:
        pk -- the pk of the room
        Return: the Room object of a room's pk, or NotFound
        """

        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        """handling the request about 'PUT /wishlists/{ID of a wishlist}/rooms/{ID of a room}'

        Keyword arguments:
        request -- the request that a user make
        pk -- the primary key or the requested wishlist
        room_pk -- the pk of the room
        Return: the serialized data of the wishlist with 'the pk & the user' which is UPDATED
        """

        wishlist = self.get_wishlist(pk, request.user)
        room = self.get_room(room_pk)

        if wishlist.rooms.filter(pk=room_pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)

        return Response(status=HTTP_200_OK)
