from django.db import models

from apps.core.models import TimestampedModel
from apps.studygroup.models.member import StudyGroupMember
from apps.studygroup.models.studygroup import StudyGroup


class AssignmentRequest(TimestampedModel):
    studygroup = models.ForeignKey(
        StudyGroup, on_delete=models.CASCADE, related_name="assignments"
    )
    author = models.ForeignKey(
        StudyGroupMember, on_delete=models.CASCADE, related_name="assignments"
    )
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=1500)

    def __str__(self) -> str:
        return f"{self.author}의 {self.title} 과제 요청"


class AssignmentSubmission(TimestampedModel):
    class Meta:
        verbose_name = "StudyGroup Assignment Submission"
        verbose_name_plural = "StudyGroup Assignment Submissions"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "assignment"], name="unique_assignment_submission"
            )
        ]

    studygroup = models.ForeignKey(
        StudyGroup, on_delete=models.CASCADE, related_name="submissions"
    )
    author = models.ForeignKey(
        StudyGroupMember, on_delete=models.CASCADE, related_name="submissions"
    )
    assignment = models.ForeignKey(
        AssignmentRequest,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=1500)

    def __str__(self) -> str:
        return f"{self.author}의 {self.assignment} 과제 제출"
