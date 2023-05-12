from rest_framework import serializers
from .models import Booking


class PublicBookingSerializer(serializers.ModelSerializer):

    """the Booking serializer for public user"""

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
