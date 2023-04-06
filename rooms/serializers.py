from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import UserSerializerForRoomDetail
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer


class AmenitiySerializer(ModelSerializer):
    """Serializer Definition for Amenity"""

    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):
    """Serailizer Definition for Room Detail"""

    # models that have a relation with a room
    owner = UserSerializerForRoomDetail(read_only=True)
    # amenities = AmenitiySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    # average review field
    avg_rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    # the method calculating the average of the rating
    def get_avg_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    # def create(self, validated_data):
    #     print(validated_data)
    #     return


class RoomListSerializer(ModelSerializer):
    """Serailizer Definition for Room List"""

    # avg ratings
    avg_rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "avg_rating",
            "is_owner",
        )
        my = [
            "as",
            "Asd",
        ]

    # calculating avg ratings
    def get_avg_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
