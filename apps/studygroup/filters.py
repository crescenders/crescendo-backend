from django.db.models import Count, F, Q
from django.utils.datetime_safe import date
from django_filters import rest_framework as filters

from apps.studygroup.models import Category, StudyGroup, Tag


class StudyGroupListFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("deadline", "deadline"),
        ),
        help_text="스터디그룹을 정렬합니다. ex) 'created_at' 정렬 시, 최신순으로 정렬됩니다.",
    )
    post_title = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        help_text="제목 검색입니다. LIKE 검색을 지원합니다. ex) 'sup' 검색 시 'wassup!', 'superman' 등이 검색됩니다.",
    )
    study_name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        help_text="스터디 이름 검색입니다. LIKE 검색을 지원합니다. ex) '스터디' 검색 시 '스터디그룹', '스터디' 등이 검색됩니다.",
    )
    is_closed = filters.BooleanFilter(
        label="is_closed",
        method="filter_is_closed",
        help_text="모집 마감 여부에 따라 스터디그룹을 보여줍니다. 값이 지정되지 않을 시, 모집 마감 여부에 상관없이 모든 스터디그룹을 보여줍니다.",
    )
    random = filters.NumberFilter(
        label="random",
        method="filter_random",
        help_text="랜덤 갯수의 스터디그룹을 보여줍니다.",
    )
    tags = filters.ModelMultipleChoiceFilter(
        conjoined=True,
        field_name="tags__name",
        to_field_name="name",
        lookup_expr="exact",
        queryset=Tag.objects.all(),
        help_text="스터디그룹의 태그를 필터링합니다. ex) 'python' 검색 시, 'python' 태그가 포함된 스터디그룹을 보여줍니다.",
    )
    categories = filters.ModelMultipleChoiceFilter(
        conjoined=True,
        field_name="categories__name",
        to_field_name="name",
        lookup_expr="exact",
        queryset=Category.objects.all(),
        help_text="스터디그룹의 카테고리를 필터링합니다. ex) '개발' 검색 시, '개발' 카테고리가 포함된 스터디그룹을 보여줍니다.",
    )

    @staticmethod
    def filter_is_closed(queryset, name, value):
        """
        모집 마감에 따라 스터디그룹을 필터링합니다.
        """
        filtered_queryset = queryset.annotate(members_count=Count("members")).filter(
            Q(deadline__lt=date.today()) | Q(members_count=F("member_limit"))
        )
        if value is True:
            return filtered_queryset
        else:
            return queryset.exclude(id__in=filtered_queryset)

    @staticmethod
    def filter_random(queryset, name, value):
        """
        숫자에 따라 랜덤으로 스터디그룹을 필터링합니다.
        """
        random_queryset = queryset.order_by("?")[:value]
        return random_queryset

    class Meta:
        model = StudyGroup
        fields = [
            "post_title",
            "study_name",
        ]
