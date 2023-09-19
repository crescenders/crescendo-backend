from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from nh3 import clean_text

from apps.studygroup import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


class StudyGroupMemberInline(admin.TabularInline):
    verbose_name = "스터디그룹 멤버"
    verbose_name_plural = "스터디그룹 멤버들"
    model = models.StudyGroupMember
    extra = 0


@admin.register(models.StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    readonly_fields = (
        "head_image_tag",
        "uuid",
        "created_at",
        "updated_at",
    )
    list_display = (
        "head_image_tag",
        "name",
        "title",
        "member_limit",
        "is_closed",
        "deadline",
    )
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
                    "head_image_tag",
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

    @staticmethod
    @admin.display(description="Head image")
    def head_image_tag(obj):
        image_url = obj.head_image.url if obj.head_image else obj.default_head_image
        return format_html('<img src="{}" style="width: 210px;" />', image_url)

    @admin.display(boolean=True)
    def is_closed(self, instance):
        return instance.is_closed

    inlines = [
        StudyGroupMemberInline,
    ]
