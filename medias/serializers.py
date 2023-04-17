from rest_framework.serializers import ModelSerializer
from .models import Photo


class PhotoSerializer(ModelSerializer):
    """the serializer for Photo

    Keyword arguments:
    model -- Photo Model
    fields -- pk(readl_only), file(required), desecription(required) of the Photo

    no-return : there's no return value
    """

    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )
