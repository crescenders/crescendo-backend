import uuid

from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.datetime_safe import date

from apps.accounts.models import User
from core.utils.models import TimestampedModel


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(
        max_length=20, unique=True, validators=[MinLengthValidator(1)]
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class StudyGroupMember(models.Model):
    class Meta:
        verbose_name = "StudyGroup Member"
        verbose_name_plural = "StudyGroup Members"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "study_group"], name="unique_study_group_member"
            )
        ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="study_group_member"
    )
    is_leader = models.BooleanField(default=False)
    study_group = models.ForeignKey(
        "StudyGroup", on_delete=models.CASCADE, related_name="members"
    )

    def __str__(self):
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
    categories = models.ManyToManyField(Category, related_name="study_groups")
    tags = models.ManyToManyField(Tag, related_name="study_groups", blank=True)

    @property
    def default_head_image(self):
        return f"https://picsum.photos/seed/{self.uuid}/210/150"

    @property
    def leaders(self):
        return self.members.filter(is_leader=True)

    @property
    def current_member_count(self):
        return self.members.count()

    @property
    def is_closed(self):
        """
        스터디그룹이 모집이 완료되었는지 여부를 반환합니다.
        1. 오늘 날짜 > deadline
        2. 현재 인원 == member_limit
        3. 현재 인원 < member_limit and 오늘 날짜 > deadline
        """
        return (
            date.today() > self.deadline
            or self.members.count() == self.member_limit
            or (
                self.members.count() < self.member_limit
                and date.today() > self.deadline
            )
        )

    def __str__(self):
        return self.name
