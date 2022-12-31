from django.db import models
from common.models import CommonModel


class Category(CommonModel):

    """Room and Experience Category"""

    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}"
