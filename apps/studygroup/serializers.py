from django.utils.datetime_safe import date
from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.studygroup import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["name"]


class LeaderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    _links = serializers.SerializerMethodField()

    class Meta:
        model = models.StudyGroupMember
        fields = [
            "username",
            "_links",
        ]

    def get__links(self, obj):
        request = self.context["request"]
        links = {
            "self": {
                "href": reverse(
                    "user_profile_uuid", kwargs={"uuid": obj.user.uuid}, request=request
                )
            },
        }
        return links


class StudyGroupListSerializer(serializers.ModelSerializer):
    leaders = LeaderSerializer(many=True, read_only=True)
    post_title = serializers.CharField(source="title")
    post_content = serializers.CharField(source="content", write_only=True)
    study_name = serializers.CharField(source="name")
    start_date = serializers.DateField(write_only=True)
    end_date = serializers.DateField(write_only=True)
    deadline = serializers.DateField(write_only=True)
    until_deadline = serializers.SerializerMethodField(read_only=True)
    is_closed = serializers.SerializerMethodField()
    current_member_count = serializers.IntegerField(
        source="members.count", read_only=True
    )
    categories = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        queryset=models.Category.objects.all(),
    )
    tags = serializers.SlugRelatedField(
        slug_field="name", many=True, queryset=models.Tag.objects.all()
    )
    _links = serializers.SerializerMethodField()

    class Meta:
        model = models.StudyGroup
        fields = [
            "head_image",
            "leaders",
            "post_title",
            "post_content",
            "study_name",
            "start_date",
            "end_date",
            "deadline",
            "until_deadline",
            "is_closed",
            "tags",
            "categories",
            "current_member_count",
            "member_limit",
            "until_deadline",
            "_links",
        ]

    @staticmethod
    def get_leaders(obj):
        return [leader.user.username for leader in obj.leaders]

    @staticmethod
    def get_until_deadline(obj) -> int:
        return (obj.deadline - date.today()).days

    @staticmethod
    def get_is_closed(obj) -> bool:
        return obj.is_closed

    def get__links(self, obj) -> dict[str, dict[str, str]]:
        request = self.context["request"]
        links = {
            "self": {
                "href": reverse(
                    "studygroup_detail", kwargs={"uuid": obj.uuid}, request=request
                )
            },
        }
        return links
