from rest_framework import serializers

from studygroup import models


class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudyGroup
        fields = [
            "uuid",
            "name",
            "user_limit",
            "start_date",
            "end_date",
            "deadline",
            "head_image",
            "title",
            "content",
            "leader",
            "categories",
            "tags",
            "members",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["name"]
