import uuid

from django.db import models

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

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # StudyGroup Fields
    name = models.CharField(max_length=80)
    user_limit = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    deadline = models.DateField()

    # StudyGroup Post Fields
    head_image = models.ImageField(upload_to="studygroup/head_image", blank=True)
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=3000)

    # Foreign Keys
    leader = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name="study_groups")
    tags = models.ManyToManyField(Tag, related_name="study_groups")

    def __str__(self):
        return f"<StudyGroup {self.name}>"
