import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.accounts.models import User
from core.utils.models import TimestampedModel


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"<Tag {self.name}>"


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"<Category {self.name}>"


class StudyGroup(TimestampedModel):
    class Meta:
        verbose_name = "StudyGroup"
        verbose_name_plural = "StudyGroups"

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
    head_image = models.ImageField(upload_to="studygroup/head_image", blank=True)
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=3000)
    deadline = models.DateField()

    # Foreign Keys
    leader = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="managing_study_groups"
    )
    members = models.ManyToManyField(
        User, related_name="joined_study_groups", blank=True
    )
    categories = models.ManyToManyField(Category, related_name="study_groups")
    tags = models.ManyToManyField(Tag, related_name="study_groups", blank=True)

    def __str__(self):
        return f"<StudyGroup {self.name}>"
