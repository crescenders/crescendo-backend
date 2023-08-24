from django.contrib import admin
from django.utils import timezone

from apps.studygroup import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StudyGroupMember)
class StudyGroupMemberAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid", "created_at", "updated_at")
    fieldsets = (
        (
            "메타 정보",
            {
                "fields": (
                    "uuid",
                    "name",
                    "created_at",
                    "updated_at",
                )
            },
        ),
        (
            "게시물 정보",
            {
                "fields": (
                    "head_image",
                    "title",
                    "content",
                    "categories",
                    "tags",
                )
            },
        ),
        (
            "모집 정보",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "deadline",
                    "member_limit",
                )
            },
        ),
    )

    list_display = (
        "name",
        "member_limit",
        "is_closed",
        "current_member_count",
        "deadline",
    )

    def is_closed(self, instance):
        return instance.is_closed

    is_closed.boolean = True

    class StudyGroupMemberInline(admin.TabularInline):
        verbose_name = "스터디그룹 멤버"
        verbose_name_plural = "스터디그룹 멤버들"
        model = models.StudyGroupMember
        extra = 0

    inlines = [
        StudyGroupMemberInline,
    ]
