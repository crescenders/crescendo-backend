from rest_framework import serializers

from apps.studygroup import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["name"]


class PromotionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PromotionPost
        fields = "__all__"


class StudyGroupSerializer(serializers.ModelSerializer):
    posts = PromotionPostSerializer(many=True)
    categories = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    tags = serializers.SlugRelatedField(
        many=True, queryset=models.Tag.objects.all(), slug_field="name"
    )

    class Meta:
        model = models.StudyGroup
        fields = [
            "uuid",
            "name",
            "user_limit",
            "start_date",
            "end_date",
            "posts",
            "categories",
            "tags",
            "studygroup_members",
        ]
