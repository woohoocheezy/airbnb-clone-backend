from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import UserSerializerForRoomDetail
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

    owner = UserSerializerForRoomDetail(read_only=True)
    amenities = AmenitiySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    # def create(self, validated_data):
    #     print(validated_data)
    #     return


class RoomListSerializer(ModelSerializer):
    """Serailizer Definition for Room List"""

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
