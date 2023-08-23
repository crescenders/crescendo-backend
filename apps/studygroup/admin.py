from django.contrib import admin
from django.utils import timezone

from apps.studygroup import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "member_limit",
        "leader",
        "is_closed",
        "deadline",
    )

    def is_closed(self, instance):
        return timezone.now().date() > instance.deadline

    is_closed.boolean = True
