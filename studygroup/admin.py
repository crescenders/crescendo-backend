from django.contrib import admin

from studygroup import models


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
        "user_limit",
        "start_date",
        "end_date",
        "deadline",
        "title",
        "content",
        "leader",
    )
