from typing import Any

from django.db.models import Count, F, Q, QuerySet
from django.utils.datetime_safe import date
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from apps.studygroup.models import Category, StudyGroup


class MyStudyGroupFilter(filters.FilterSet):  # type: ignore
    filter = filters.TypedChoiceFilter(
        label="filter",
        choices=(
            (
                "current",
                "현재 사용자가 가입해 활동 중인 스터디그룹들, 모집이 닫히고 활동이 시작된 스터디그룹들을 필터링합니다.",
            ),
            (
                "requested",
                "현재 사용자가 가입 요청해서 승인을 기다리고 있는 스터디그룹들을 필터링합니다.",
            ),
            (
                "approved",
                "현재 사용자가 가입을 요청했고, 승인되었지만 아직 활동을 시작하지 않은 스터디그룹들을 필터링합니다.",
            ),
            (
                "disapproved",
                "현재 사용자가 가입을 요청했지만, 거절당한 스터디그룹들",
            ),
            (
                "as_leader",
                "현재 사용자가 리더인 스터디그룹들",
            ),
        ),
        method="filter_my_studygroup",
        help_text="검색 조건에 따라 나와 관련된 스터디그룹을 필터링합니다.",
    )

    def filter_my_studygroup(
        self, queryset: QuerySet[StudyGroup], name: str, value: str
    ) -> QuerySet[StudyGroup]:
        if value == "current":
            return self._filter_current(queryset)
        elif value == "requested":
            return self._filter_requested(queryset)
        elif value == "approved":
            return self._filter_approved(queryset)
        elif value == "disapproved":
            return self._filter_disapproved(queryset)
        elif value == "as_leader":
            return self._filter_as_leader(queryset)
        return queryset

    def _filter_current(self, queryset: QuerySet[StudyGroup]) -> QuerySet[StudyGroup]:
        """
        현재 사용자가 가입해 활동 중인 스터디그룹들을 필터링합니다.
        """
        queryset = queryset.filter(
            members__user__in=[self.request.user],
            members__is_leader=False,
            start_date__lte=date.today(),  # 활동 시작일이 오늘보다 이전
            end_date__gte=date.today(),  # 활동 종료일이 오늘보다 이후
        )
        return queryset

    def _filter_requested(self, queryset: QuerySet[StudyGroup]) -> QuerySet[StudyGroup]:
        """
        현재 사용자가 가입 요청해서 승인을 기다리고 있는 스터디그룹들을 필터링합니다.
        모집 마감일이 지나지 않고, 모집 인원이 남아있어야 합니다.
        """
        queryset = queryset.annotate(
            members_count=Count("members"),
        ).filter(
            requests__user__in=[self.request.user],
            requests__processed=False,
            requests__is_approved=False,
            deadline__gt=date.today(),  # 모집 마감일이 지나지 않음
            member_limit__gt=F("members_count"),  # 모집 인원이 남음
        )
        return queryset

    def _filter_approved(self, queryset: QuerySet[StudyGroup]) -> QuerySet[StudyGroup]:
        """
        현재 사용자가 가입을 요청했고, 승인되었지만 아직 활동을 시작하지 않은 스터디그룹들을 필터링합니다.
        """
        queryset = queryset.filter(
            members__user__in=[self.request.user],
            members__is_leader=False,
            start_date__gte=date.today(),  # 활동 시작일이 오늘보다 이후
        )
        return queryset

    def _filter_disapproved(
        self, queryset: QuerySet[StudyGroup]
    ) -> QuerySet[StudyGroup]:
        """
        현재 사용자가 가입을 요청했지만, 거절당한 스터디그룹들을 필터링합니다.
        """
        queryset = queryset.filter(
            requests__user__in=[self.request.user],
            requests__processed=True,
            requests__is_approved=False,
        )
        return queryset

    def _filter_as_leader(self, queryset: QuerySet[StudyGroup]) -> QuerySet[StudyGroup]:
        """
        현재 사용자가 리더인 스터디그룹들을 필터링합니다.
        """
        queryset = queryset.filter(
            members__user__in=[self.request.user],
            members__is_leader=True,
        )
        return queryset

    class Meta:
        model = StudyGroup
        fields: list[Any] = []


class StudyGroupOrderingFilter(OrderingFilter):  # type: ignore
    additional_filters = ["random"]
    fields_related = {"random": "?"}
    ordering_fields = ("created_at", "deadline", "random")

    def get_ordering(self, request, queryset, view):
        """
        OrderingFilter 의 get_ordering 메서드를 오버라이딩합니다.
        random 은 모델의 필드가 아니므로 rest_framework 의 기본 get_ordering 에서 처리할 수 없습니다.
        하여 random 쿼리스트링이 들어오면, fields_related 에서 해당하는 필드를 가져와서 처리합니다.
        """
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(",")]
            valid_ordering_fields = [
                self.fields_related.get(f.lstrip("-"))
                for f in fields
                if f.lstrip("-") in self.additional_filters
            ]
            if valid_ordering_fields:
                return valid_ordering_fields
        return super().get_ordering(request, queryset, view)

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            if "random" in ordering:
                return queryset.order_by("?")
            return queryset.order_by(*ordering)
        return queryset

    def get_template_context(self, request, queryset, view):
        """
        BrowseableAPIRenderer 에서 사용하는 템플릿 컨텍스트를 커스터마이징합니다.
        random 일 경우, "ascending" 혹은 "descending" 을 표시하지 않습니다.
        """
        current = self.get_ordering(request, queryset, view)
        current = None if not current else current[0]
        options = []
        context = {
            "request": request,
            "current": current,
            "param": self.ordering_param,
        }
        for key, label in self.get_valid_fields(queryset, view, context):
            if key == "random":
                options.append((key, label))
                continue
            options.append((key, "%s - %s" % (label, _("ascending"))))
            options.append(("-" + key, "%s - %s" % (label, _("descending"))))
        context["options"] = options
        return context


class StudyGroupListFilter(filters.FilterSet):  # type: ignore
    post_title = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        help_text=(
            "제목 검색입니다. LIKE 검색을 지원합니다. ex) 'sup' 검색 시 'wassup!', 'superman' 등이 검색됩니다."
        ),
    )
    study_name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        help_text=(
            "스터디 이름 검색입니다. LIKE 검색을 지원합니다. ex) '스터디' 검색 시 '스터디그룹', '스터디' 등이 검색됩니다."
        ),
    )
    is_closed = filters.BooleanFilter(
        label="is_closed",
        method="filter_is_closed",
        help_text=(
            "모집 마감 여부에 따라 스터디그룹을 보여줍니다. 값이 지정되지 않을 시, 모집 마감 여부에 상관없이 모든 스터디그룹을 보여줍니다."
        ),
    )
    tags = filters.CharFilter(
        field_name="tags__name",
        lookup_expr="exact",
        help_text=(
            "스터디그룹의 태그를 필터링합니다. ex) 'python' 검색 시, 'python' 태그가 포함된 스터디그룹을 보여줍니다."
        ),
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
    def filter_is_closed(
        queryset: QuerySet[StudyGroup], name: str, value: bool
    ) -> QuerySet[StudyGroup]:
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

    class Meta:
        model = StudyGroup
        fields = [
            "post_title",
            "study_name",
        ]
