from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from django.db import transaction
from .models import Amenity, Room
from .serializers import AmenitiySerializer, RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer
from categories.models import Category
from django.conf import settings


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
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
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

                # apply django db transaction for amenities
                try:
                    with transaction.atomic():
                        room = serializer.save(
                            owner=request.user,
                            category=category,
                        )

                        # get amenity 'pk's from user request
                        amenities = request.data.get("amenities")

                        # add a amenity to room
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)

                        return Response(RoomDetailSerializer(room).data)
                except Exception:
                    raise ParseError("Amenity not found")

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
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)

        # check if the user is authenticated
        if not request.user.is_authenticated:
            raise NotAuthenticated

        # check if the user is same with owner of the room
        if room.owner != request.user:
            raise PermissionDenied

        # update
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )

        # check if the information from the serializer is valid
        if serializer.is_valid():
            # check if the category is given from user request
            category_pk = request.data.get("category")

            # if user wants to update this room's category
            # check if the category is valid
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)

                    # check if the category kind is room
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")

                # the case when the given category is not available from DB
                except Category.DoesNotExist:
                    raise ParseError("Category not found")

            try:
                with transaction.atomic():
                    # if the category is given, create a updated room wtih the category
                    if category_pk:
                        updated_room = serializer.save(
                            category=category,
                        )
                    # if the category is not given, create a updated room without the category
                    else:
                        updated_room = serializer.save()

                    # get amenity 'pk's from user request
                    amenities = request.data.get("amenities")

                    # the case which user wants to update
                    if amenities:
                        # clear the existing amenities on the room
                        updated_room.amenities.clear()

                        # add new amenities to the room
                        # if any amenity is not on DB, the ParseError is raised
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            updated_room.amenities.add(amenity)

                    return Response(RoomDetailSerializer(updated_room).data)

            except Exception as e:
                # the case Amenity with given pks is not found
                raise ParseError("Amenity not found")

        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)

        # check if the user is authenticated
        if not request.user.is_authenticated:
            raise NotAuthenticated

        # check if the user is same with the owner of this room
        if room.owner != request.user:
            raise PermissionDenied

        room.delete()
        return Response(HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:  # the case lie ?page='adasda'
            page = 1  # at this case set 'page' as '1' instead of sending error message

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )

        return Response(serializer.data)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:  # the case lie ?page='adasda'
            page = 1  # at this case set 'page' as '1' instead of sending error message

        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitiySerializer(
            room.amenities.all()[start:end],
            many=True,
        )

        return Response(serializer.data)


class RoomPhotos(APIView):
    def post(self, request, pk):
        pass
