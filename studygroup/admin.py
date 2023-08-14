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
    class PromotionPostInline(admin.TabularInline):
        model = models.PromotionPost
        extra = 0

    class StudyGroupMemberInline(admin.TabularInline):
        model = models.StudyGroupMember
        extra = 0

    list_display = (
        "name",
        "user_limit",
        "start_date",
        "end_date",
    )
    filter_horizontal = ("categories", "tags")
    inlines = (StudyGroupMemberInline, PromotionPostInline)
