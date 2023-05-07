from rest_framework import serializers
from users.serializers import UserSerializerForRoomDetail
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializerForRoomDetail(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )
