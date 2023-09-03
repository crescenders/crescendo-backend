from django_filters import rest_framework as filters

from apps.studygroup.models import StudyGroup


class StudyGroupFilter(filters.FilterSet):
    post_title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    post_content = filters.CharFilter(field_name="content", lookup_expr="icontains")

    # tags = filters.AllValuesMultipleFilter(field_name="tags__name")

    class Meta:
        model = StudyGroup
        fields = [
            "post_title",
            "post_content",
        ]
