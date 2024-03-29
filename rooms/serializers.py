from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import UserSerializerForRoomDetail
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


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
    is_liked = serializers.SerializerMethodField()

    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    # the method calculating the average of the rating
    def get_avg_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()

    # def create(self, validated_data):
    #     print(validated_data)
    #     return


class RoomListSerializer(ModelSerializer):
    """Serailizer Definition for Room List"""

    # avg ratings
    avg_rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    photos = PhotoSerializer(many=True, read_only=True)

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
            "photos",
        )

    # calculating avg ratings
    def get_avg_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user


class HostRoomSerializer(ModelSerializer):
    total_amenities = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "country",
            "city",
            "price",
            "rooms",
            "toilets",
            "description",
            "address",
            "pet_friendly",
            "kind",
            "total_amenities",
            "total_reviews",
            "rating",
        )

    def get_total_amenities(self, room):
        return room.total_amenities()

    def get_total_reviews(self, room):
        return room.total_reviews()

    def get_rating(self, room):
        return room.rating()
