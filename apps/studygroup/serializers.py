from django.utils.datetime_safe import date
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.studygroup import models
from core.utils.serializers import CreatableSlugRelatedField


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

    @extend_schema_field(
        {
            "example": [
                {
                    "rel": "self",
                    "href": "http://localhost:8000/api/v1/user/profile/uuid/",
                },
            ],
        }
    )
    def get__links(self, obj):
        request = self.context["request"]
        links = [
            {
                "rel": "self",
                "href": reverse(
                    "user_profile_uuid",
                    kwargs={"uuid": obj.user.uuid},
                    request=request,
                ),
            }
        ]
        return links


class StudyGroupListSerializer(serializers.ModelSerializer):
    # 헤더 이미지, 제목, 내용
    head_image = serializers.SerializerMethodField()
    post_title = serializers.CharField(source="title")
    post_content = serializers.CharField(source="content", write_only=True)

    # 리터, 스터디 이름
    leaders = LeaderSerializer(many=True, read_only=True)
    study_name = serializers.CharField(source="name")

    # 스터디 시작일, 종료일, 모집 마감일
    start_date = serializers.DateField(write_only=True)
    end_date = serializers.DateField(write_only=True)
    deadline = serializers.DateField(write_only=True)
    until_deadline = serializers.SerializerMethodField(read_only=True)

    # 마감 여부, 현재 인원
    is_closed = serializers.SerializerMethodField()
    current_member_count = serializers.IntegerField(
        source="members.count", read_only=True
    )

    # Category, Tag
    categories = serializers.SlugRelatedField(
        many=True, queryset=models.Category.objects.all(), slug_field="name"
    )
    tags = CreatableSlugRelatedField(
        many=True, queryset=models.Tag.objects.all(), slug_field="name"
    )

    # hateoas
    _links = serializers.SerializerMethodField()

    class Meta:
        model = models.StudyGroup
        fields = [
            "uuid",
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

    @extend_schema_field(
        {
            "example": "https://picsum.photos/seed/uuid/210/150",
        }
    )
    def get_head_image(self, obj):
        return (
            serializers.ImageField.to_representation(self, obj.head_image)
            if serializers.ImageField.to_representation(self, obj.head_image)
            is not None
            else obj.default_head_image
        )

    @staticmethod
    def get_leaders(obj):
        return [leader.user.username for leader in obj.leaders]

    @staticmethod
    def get_until_deadline(obj) -> int:
        return (obj.deadline - date.today()).days

    @staticmethod
    def get_is_closed(obj) -> bool:
        return obj.is_closed

    @extend_schema_field(
        {
            "example": [
                {
                    "rel": "self",
                    "href": "http://localhost:8000/api/v1/studygroup/uuid/",
                },
            ],
        }
    )
    def get__links(self, obj):
        request = self.context["request"]
        links = (
            [
                {
                    "rel": "self",
                    "href": reverse(
                        "studygroup_detail", kwargs={"uuid": obj.uuid}, request=request
                    ),
                },
            ],
        )

        return links


class StudyGroupDetailSerializer(StudyGroupListSerializer):
    post_content = serializers.CharField(source="content")
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    deadline = serializers.DateField()

    class Meta:
        model = models.StudyGroup
        fields = [
            "head_image",
            "leaders",
            "post_title",
            "post_content",
            "created_at",
            "updated_at",
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
