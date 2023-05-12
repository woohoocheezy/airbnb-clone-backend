from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    """the Booking serializer for handling user's request to create a booking for a room"""

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        """if you use this serailizer for create a room booking, 'check_in' and 'check_out' are required, not optional."""

        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        """validate whether 'check_in' is later than now

        Keyword arguments:
        value -- 'check_in' data which type is DateField()
        Return: the value('check_in' data) if the value is valid
        """

        now = timezone.localtime(timezone.now()).date()

        if now > value:
            raise serializers.ValidationError("Can't book in the past!")

        return value

    def validate_check_out(self, value):
        """validate whether 'check_out' is later than now

        Keyword arguments:
        value -- 'check_out' data which type is DateField()
        Return: the value('check_out' data) if the value is valid
        """

        now = timezone.localtime(timezone.now()).date()

        if now > value:
            raise serializers.ValidationError("Can't book in the past!")

        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check In should be earlier than Check Out."
            )

        if Booking.objects.filter(
            check_in__lt=data["check_out"],
            check_out__gt=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken."
            )

        return data


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
