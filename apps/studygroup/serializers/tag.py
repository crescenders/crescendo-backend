from rest_framework import serializers

from apps.studygroup.models import Tag


class TagReadSerializer(serializers.ModelSerializer[Tag]):
    """
    태그 목록을 조회하기 위한 serializer 입니다.
    """

    class Meta:
        model = Tag
        fields = ["name"]
