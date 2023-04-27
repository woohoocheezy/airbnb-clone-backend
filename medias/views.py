from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Photo


class PhotoDetail(APIView):
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        """delete photos of a room with a room pk

        Keyword arguments:
        pk -- the pk of the room
        Return: Response(HTTP_200_OK)
        """

        photo = self.get_object(pk)

        # if photo.room:
        #     if photo.room.owner != request.user:  # using 2 relations via ORM
        #         raise PermissionDenied
        # elif photo.experience:
        #     if photo.experience.host != request.user:
        #         raise PermissionDenied

        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied

        photo.delete()

        return Response(status=HTTP_200_OK)

        # return super().delete(request, *args, **kwargs)
