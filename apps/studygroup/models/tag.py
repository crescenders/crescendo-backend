from django.core.validators import MinLengthValidator
from django.db import models


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(
        max_length=20, unique=True, validators=[MinLengthValidator(1)]
    )

    def __str__(self) -> str:
        return self.name
