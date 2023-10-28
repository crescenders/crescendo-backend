from django.contrib import admin

from apps.studygroup.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin[Tag]):
    list_display = (
        "id",
        "name",
    )
