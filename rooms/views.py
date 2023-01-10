from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Amenity
from .serializers import AmenitiySerializer


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
    Amenity API URL for "GET", "POST" and "DELETE" request
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
