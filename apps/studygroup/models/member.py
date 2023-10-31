from typing import Any

from django.core.exceptions import ValidationError
from django.db import models

from apps.accounts.models import User
from apps.core.models import TimestampedModel


class StudyGroupMemberRequest(models.Model):
    """
    스터디그룹 가입 요청 모델
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="studygroup_member_request"
    )
    studygroup = models.ForeignKey(
        "StudyGroup", on_delete=models.CASCADE, related_name="requests"
    )
    created_at = models.DateTimeField(auto_now_add=True)  # 신청 시간
    request_message = models.CharField(max_length=200, blank=False)
    processed = models.BooleanField(default=False)  # 최종 처리 여부
    is_approved = models.BooleanField(default=False)  # 승인 여부

    def __str__(self) -> str:
        return f"{self.user.username}의 {self.studygroup} 로 가입 요청"

    def clean(self) -> None:
        if self.is_approved is True and self.processed is False:
            raise ValidationError("is_approved가 True이면 processed는 True여야 합니다.")

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class StudyGroupMember(TimestampedModel):
    class Meta:
        verbose_name = "StudyGroup Member"
        verbose_name_plural = "StudyGroup Members"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "studygroup"], name="unique_studygroup_member"
            )
        ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="studygroup_member"
    )
    is_leader = models.BooleanField(default=False)
    studygroup = models.ForeignKey(
        "StudyGroup", on_delete=models.CASCADE, related_name="members"
    )

    def __str__(self) -> str:
        if self.is_leader is True:
            return f"리더 멤버 {self.user.username}"
        return f"일반 멤버 {self.user.username}"
