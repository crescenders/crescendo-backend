from typing import Any

from django.contrib import admin
from django.db.models import ForeignKey
from django.forms import ModelChoiceField
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from apps.studygroup.models import (
    AssignmentRequest,
    AssignmentSubmission,
    StudyGroup,
    StudyGroupMember,
    StudyGroupMemberRequest,
)


class StudyGroupMemberInline(admin.TabularInline[StudyGroupMember, StudyGroup]):
    verbose_name = "스터디그룹 멤버"
    verbose_name_plural = "스터디그룹 멤버들"
    model = StudyGroupMember
    extra = 0


class StudyGroupMemberRequestInline(
    admin.TabularInline[StudyGroupMemberRequest, StudyGroup]
):
    verbose_name = "스터디그룹 가입 요청"
    verbose_name_plural = "스터디그룹 가입 요청들"
    model = StudyGroupMemberRequest
    extra = 0


class StudyGroupAssignmentRequestInline(
    admin.TabularInline[AssignmentRequest, StudyGroup]
):
    verbose_name = "스터디그룹 과제 요청"
    verbose_name_plural = "스터디그룹 과제 요청들"
    model = AssignmentRequest
    extra = 0

    def formfield_for_foreignkey(
        self, db_field: ForeignKey, request: HttpRequest, **kwargs: Any
    ) -> ModelChoiceField:
        if db_field.name == "author":
            assert request.resolver_match is not None
            studygroup_id = request.resolver_match.kwargs["object_id"]
            kwargs["queryset"] = StudyGroupMember.objects.filter(
                studygroup_id=studygroup_id, is_leader=True
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class StudyGroupAssignmentSubmissionInline(
    admin.TabularInline[AssignmentRequest, StudyGroup]
):
    verbose_name = "스터디그룹 과제 제출"
    verbose_name_plural = "스터디그룹 과제 제출들"
    model = AssignmentSubmission
    extra = 0

    def formfield_for_foreignkey(
        self, db_field: ForeignKey, request: HttpRequest, **kwargs: Any
    ) -> ModelChoiceField:
        if db_field.name == "author":
            assert request.resolver_match is not None
            studygroup_id = request.resolver_match.kwargs["object_id"]
            kwargs["queryset"] = StudyGroupMember.objects.filter(
                studygroup_id=studygroup_id
            )
        if db_field.name == "assignment":
            assert request.resolver_match is not None
            studygroup_id = request.resolver_match.kwargs["object_id"]
            kwargs["queryset"] = AssignmentRequest.objects.filter(
                studygroup_id=studygroup_id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin[StudyGroup]):
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
        "leaders",
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

    def response_change(self, request: HttpRequest, obj: StudyGroup) -> HttpResponse:
        if "_save" in request.POST:
            change_url = reverse(
                "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
                args=[obj.pk],
            )
            return HttpResponseRedirect(change_url)

        return super().response_change(request, obj)

    @staticmethod
    @admin.display(description="Head image")
    def head_image_tag(obj: StudyGroup) -> str:
        image_url = obj.head_image.url if obj.head_image else obj.default_head_image
        return format_html('<img src="{}" style="width: 210px;" />', image_url)

    @admin.display(description="Leaders")
    def leaders(self, instance: StudyGroup) -> str:
        return ", ".join([member.user.username for member in instance.leaders])

    @admin.display(boolean=True)
    def is_closed(self, instance: StudyGroup) -> bool:
        return instance.is_closed

    inlines = [
        StudyGroupMemberRequestInline,
        StudyGroupMemberInline,
        StudyGroupAssignmentRequestInline,
        StudyGroupAssignmentSubmissionInline,
    ]
