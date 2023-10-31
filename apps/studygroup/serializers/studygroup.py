from collections import OrderedDict
from typing import Any

from django.utils.datetime_safe import date
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.core.serializers import CreatableSlugRelatedField
from apps.studygroup.models import Category, StudyGroup, Tag
from apps.studygroup.serializers import LeaderReadSerializer


class StudyGroupListSerializer(serializers.ModelSerializer[StudyGroup]):
    # 헤더 이미지, 제목, 내용
    head_image = serializers.ImageField(required=False)
    post_title = serializers.CharField(source="title")
    post_content = serializers.CharField(source="content", write_only=True)

    # 리터, 스터디 이름
    leaders = LeaderReadSerializer(many=True, read_only=True)
    study_name = serializers.CharField(source="name")

    # 스터디 시작일, 종료일, 모집 마감일
    start_date = serializers.DateField(write_only=True)
    end_date = serializers.DateField(write_only=True)
    deadline = serializers.DateField(write_only=True)

    # Category, Tag
    categories = serializers.SlugRelatedField(
        many=True,
        required=True,
        queryset=Category.objects.all(),
        slug_field="name",
    )
    tags = CreatableSlugRelatedField(
        many=True, queryset=Tag.objects.all(), slug_field="name"
    )

    class Meta:
        model = StudyGroup
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
        ]

    @extend_schema_field(
        {
            "example": "https://picsum.photos/seed/uuid/210/150",
        },
    )
    def get_head_image(self, obj: StudyGroup) -> str:
        return (
            serializers.ImageField.to_representation(self, obj.head_image)
            if serializers.ImageField.to_representation(self, obj.head_image)
            is not None
            else obj.default_head_image
        )

    @staticmethod
    def validate_start_date(value: date) -> date:
        if value < date.today():
            raise serializers.ValidationError(
                "The studygroup's study start date must be after today."
            )
        return value

    @staticmethod
    def validate_categories(value: list[Category]) -> list[Category]:
        if not value:
            raise serializers.ValidationError(
                'You must specify at least one "categories" field.'
            )
        return value

    def to_representation(self, instance: StudyGroup) -> OrderedDict[str, Any]:
        ret = super().to_representation(instance)
        if not ret["head_image"]:
            ret["head_image"] = self.get_head_image(instance)
        return ret

    def validate(self, attrs: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        # 이미 종료된 스터디그룹이라면, 수정 불가능
        if isinstance(self.instance, StudyGroup):
            assert isinstance(
                self.instance, StudyGroup
            ), f"{self.instance} is not StudyGroup"
            if self.instance and self.instance.uuid and self.instance.is_closed is True:
                raise serializers.ValidationError(
                    "The studygroup is already closed. You can't update it."
                )
        # 날짜 검증
        if (
            not date.today()
            < attrs["deadline"]
            < attrs["start_date"]
            < attrs["end_date"]
        ):
            raise serializers.ValidationError(
                f"Each date must be: today({date.today()}) < recruitment deadline <"
                " study start date < study end date."
            )
        return attrs


class StudyGroupDetailSerializer(StudyGroupListSerializer):
    post_content = serializers.CharField(source="content")
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    deadline = serializers.DateField()

    class Meta:
        model = StudyGroup
        fields = [
            "uuid",
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
        ]


class MyStudyGroupReadSerializer(serializers.ModelSerializer[StudyGroup]):
    """
    나와 관련된 스터디그룹을 조회하기 위한 serializer 입니다.
    """

    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    categories = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = StudyGroup
        fields = [
            "uuid",
            "head_image",
            "name",
            "categories",
            "start_date",
            "end_date",
            "created_at",
            "deadline",
            "until_deadline",
            "is_closed",
            "current_member_count",
        ]

    @extend_schema_field(
        {
            "example": "https://picsum.photos/seed/uuid/210/150",
        },
    )
    def get_head_image(self, obj: StudyGroup) -> str:
        return (
            serializers.ImageField.to_representation(self, obj.head_image)
            if serializers.ImageField.to_representation(self, obj.head_image)
            is not None
            else obj.default_head_image
        )

    def to_representation(self, instance: StudyGroup) -> OrderedDict[str, Any]:
        ret = super().to_representation(instance)
        if not ret["head_image"]:
            ret["head_image"] = self.get_head_image(instance)
        return ret
