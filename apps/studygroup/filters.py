from django.db.models import Count, F, Q
from django.utils.datetime_safe import date
from django_filters import rest_framework as filters

from apps.studygroup.models import StudyGroup


class StudyGroupFilter(filters.FilterSet):
    post_title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    study_name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    is_closed = filters.BooleanFilter(label="is_closed", method="filter_is_closed")

    @staticmethod
    def filter_is_closed(queryset, name, value):
        if value is True:
            # 모집이 마감된 스터디그룹만 보여줌
            pass
        else:
            # 모집이 마감되지 않은 스터디그룹만 보여줌
            pass
        queryset = queryset.annotate(members_count=Count("members")).filter(
            Q(deadline__lt=date.today()) | Q(members_count=F("member_limit"))
        )
        return queryset

    class Meta:
        model = StudyGroup
        fields = [
            "post_title",
            "study_name",
        ]
