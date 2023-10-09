import uuid

from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import QuerySet
from django.utils.datetime_safe import date
from django.utils.functional import cached_property

from apps.accounts.models import User
from apps.core.models import TimestampedModel


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(
        max_length=20, unique=True, validators=[MinLengthValidator(1)]
    )

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name


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
    is_approved = models.BooleanField(default=False)
    request_message = models.CharField(max_length=200, blank=False)
    studygroup = models.ForeignKey(
        "StudyGroup", on_delete=models.CASCADE, related_name="members"
    )

    def __str__(self) -> str:
        return f"멤버 {self.user.username}"


class StudyGroup(TimestampedModel):
    class Meta:
        verbose_name = "StudyGroup"
        verbose_name_plural = "StudyGroups"
        ordering = ["-pk"]

    # UUID Key
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # StudyGroup Fields
    name = models.CharField(max_length=80)
    member_limit = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(10)]
    )
    start_date = models.DateField()
    end_date = models.DateField()

    # Post Fields
    head_image = models.ImageField(
        upload_to="studygroup/head_images/%Y/%m/%d", blank=True
    )
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=3000)
    deadline = models.DateField()

    # Foreign Keys
    categories = models.ManyToManyField(Category, related_name="studygroups")
    tags = models.ManyToManyField(Tag, related_name="studygroups", blank=True)

    @property
    def default_head_image(self) -> str:
        """
        스터디그룹의 기본 헤더 이미지를 반환합니다.
        """
        return f"https://picsum.photos/seed/{self.uuid}/210/150"

    @cached_property
    def approved_members(self) -> QuerySet[StudyGroupMember]:
        """
        승인된 스터디그룹원들을 반환합니다.
        """
        return self.members.filter(is_approved=True)

    @cached_property
    def leaders(self) -> QuerySet[StudyGroupMember]:
        """
        스터디그룹장들을 반환합니다.
        """
        return self.members.filter(is_leader=True)

    @cached_property
    def current_member_count(self) -> int:
        """
        현재 스터디그룹의 인원 수를 반환합니다.
        """
        return self.approved_members.count()

    @property
    def until_deadline(self) -> int:
        """
        모집 종료일까지 남은 날짜를 반환합니다.
        """
        return (self.deadline - date.today()).days

    @cached_property
    def is_closed(self) -> bool:
        """
        스터디그룹이 모집이 완료되었는지 여부를 반환합니다.
        오늘 날짜 > deadline or 현재 인원 == member_limit
        """
        return (
            date.today() > self.deadline
            or self.current_member_count == self.member_limit
        )

    def __str__(self) -> str:
        return self.name
