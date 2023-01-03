from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    """
    Photo Model Definition
    """

    file = models.ImageField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="medias",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="medias",
    )

    def __str__(self) -> str:
        return "Photo File"


class Video(CommonModel):
    """
    Video Model Definition
    """

    file = models.FileField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return "Video File"
