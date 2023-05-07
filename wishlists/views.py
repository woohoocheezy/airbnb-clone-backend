from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
