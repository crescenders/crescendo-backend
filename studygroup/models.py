import uuid

from django.db import models

from accounts.models import User
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
    user_limit = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    # Foreign Keys
    categories = models.ManyToManyField(Category, related_name="study_groups")
    tags = models.ManyToManyField(Tag, related_name="study_groups", blank=True)

    def __str__(self):
        return f"<StudyGroup {self.name}>"


class StudyGroupMember(models.Model):
    class Meta:
        verbose_name = "StudyGroup Members"
        verbose_name_plural = "StudyGroup Members"

    is_leader = models.BooleanField(default=False)
    studygroup = models.ForeignKey(
        StudyGroup, on_delete=models.CASCADE, related_name="studygroup_members"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="studygroup_members"
    )

    def __str__(self):
        return f"""<StudyGroup "{self.studygroup}", {self.user.username}>"""


class PromotionPost(TimestampedModel):
    class Meta:
        verbose_name = "Promotion Post"
        verbose_name_plural = "Promotion Posts"

    # UUID Key
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Post Fields
    head_image = models.ImageField(upload_to="studygroup/head_image", blank=True)
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=3000)
    deadline = models.DateField()

    # Foreign Keys
    study_group = models.OneToOneField("StudyGroup", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Promotion Post {self.title}>"
