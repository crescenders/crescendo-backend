from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.functional import cached_property


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(
        max_length=20, unique=True, validators=[MinLengthValidator(1)]
    )

    @cached_property
    def related_studygroups_count(self) -> int:
        """
        연관된 스터디그룹 수를 반환합니다.
        """
        return self.studygroups.count()

    def __str__(self) -> str:
        return self.name
