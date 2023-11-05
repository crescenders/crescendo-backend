from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    name = models.CharField(max_length=20, unique=True)

    @cached_property
    def related_studygroups_count(self) -> int:
        """
        연관된 스터디그룹 수를 반환합니다.
        """
        return self.studygroups.count()

    def __str__(self) -> str:
        return self.name
