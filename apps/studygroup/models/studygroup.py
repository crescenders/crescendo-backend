import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet
from django.utils.datetime_safe import date
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimestampedModel
from apps.studygroup.models.member import StudyGroupMember


class StudyGroup(TimestampedModel):
    class Meta:
        verbose_name = _("StudyGroup")
        verbose_name_plural = _("StudyGroups")
        ordering = ["-pk"]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=80)
    member_limit = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(10)]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    head_image = models.ImageField(
        upload_to="studygroup/head_images/%Y/%m/%d", blank=True
    )
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=3000)
    deadline = models.DateField()
    categories = models.ManyToManyField("Category", related_name="studygroups")
    tags = models.ManyToManyField("Tag", related_name="studygroups", blank=True)

    @property
    def default_head_image(self) -> str:
        """
        스터디그룹의 기본 헤더 이미지를 반환합니다.
        """
        return f"https://picsum.photos/seed/{self.uuid}/1080"

    @cached_property
    def approved_members(self) -> QuerySet[StudyGroupMember]:
        """
        승인된 스터디그룹원들을 반환합니다.
        """
        return self.members.all()

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
