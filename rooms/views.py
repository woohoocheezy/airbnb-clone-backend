from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Amenity, Room
from .serializers import AmenitiySerializer, RoomListSerializer, RoomDetailSerializer
from categories.models import Category


class Amenities(APIView):
    """
    Amenities API URL for "GET" and "POST" request
    example : /api/v1/rooms/amenities
    """

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitiySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitiySerializer(data=request.data)

        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitiySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    """
    Amenity API URL for "GET", "PUT" and "DELETE" request
    example : /api/v1/rooms/amenities/1
    """

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        """
        (Works same)
        amenity = self.get_object(pk)
        serializer = AmenitiySerializer(amenity)
        return Response(serializer.data)
        """

        return Response(
            AmenitiySerializer(
                self.get_object(pk),
            ).data,
        )

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitiySerializer(
            amenity,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitiySerializer(updated_amenity).data,
            )

        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):

    """
    Rooms API URL for "GET" and "POST" request
    example : /api/v1/rooms
    """

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)

            if serializer.is_valid():
                category_pk = request.data.get(
                    "category"
                )  # get catepory pk from request.data

                # category validation
                if not category_pk:  # the category pk is not given from request.data
                    raise ParseError("Category is required")

                try:  # the category pk is not valid from DB
                    category = Category.objects.get(pk=category_pk)

                    # the category kind is not Room
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")

                except Category.DoesNotExist:
                    raise ParseError("Category not found")

                room = serializer.save(
                    owner=request.user,
                    category=category,
                )

                # get amenity 'pk's from user request
                amenities = request.data.get("amenities")

                # check if 'pk's are in DB
                for amenity_pk in amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    except Amenity.DoesNotExist:
                        pass

                    # try:
                    #     amenity = Amenity.objects.get(pk=amenity_pk)
                    # except Amenity.DoesNotExist:
                    #     raise ParseError(f"Amenity with id {amenity_pk} not found")

                    # room.amenities.add(amenity)

                return Response(RoomDetailSerializer(room).data)

            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    """
    Room API URL for "GET", "PUT" and "DELETE"  request
    example : /api/v1/rooms/1
    """

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
