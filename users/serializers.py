from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializerForRoomDetail(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )
