from rest_framework import serializers

from apps.studygroup.models import Category


class CategoryReadSerializer(serializers.ModelSerializer[Category]):
    """
    카테고리 목록을 조회하기 위한 serializer 입니다.
    """

    class Meta:
        model = Category
        fields = ["name"]
