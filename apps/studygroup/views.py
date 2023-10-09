from typing import Any

from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.accounts.models import User
from apps.studygroup.filters import StudyGroupListFilter
from apps.studygroup.models import Category, StudyGroup, StudyGroupMember
from apps.studygroup.pagination import StudyGroupPagination
from apps.studygroup.permissions import IsLeaderOrReadOnly, StudyGroupAddMember
from apps.studygroup.serializers import (
    CategorySerializer,
    StudyGroupDetailSerializer,
    StudyGroupListSerializer,
    StudyGroupMemberCreateRequestBody,
    StudyGroupMemberSchema,
    StudyGroupMemberUpdateRequestBody,
)


@extend_schema(tags=["스터디그룹 관리 API"])
class StudyGroupAPISet(viewsets.ModelViewSet):
    # Serializer
    serializer_class = StudyGroupListSerializer

    # Parser
    parser_classes = (MultiPartParser, FormParser)

    # Lookup Field
    lookup_field = "uuid"

    # Permission
    permission_classes = (IsLeaderOrReadOnly,)

    # Filtering
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StudyGroupListFilter

    # Pagination
    pagination_class = StudyGroupPagination

    def get_queryset(self) -> QuerySet[StudyGroup]:
        queryset = StudyGroup.objects.all()
        if self.action in ["list"]:
            return queryset.defer("content")
        return queryset

    def get_serializer_class(self) -> type[BaseSerializer[StudyGroup]]:
        if self.action in ["list", "create"]:
            return StudyGroupListSerializer
        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return StudyGroupDetailSerializer
        return super().get_serializer_class()

    @transaction.atomic
    def perform_create(self, serializer: BaseSerializer[StudyGroup]) -> None:
        """
        스터디그룹을 생성하면, 스터디그룹장으로 자동으로 등록됩니다.
        """
        super().perform_create(serializer)
        assert isinstance(self.request.user, User)
        assert isinstance(serializer.instance, StudyGroup)
        initial_member = StudyGroupMember.objects.create(
            user=self.request.user,
            studygroup=serializer.instance,
            is_leader=True,
            is_approved=True,
        )
        serializer.instance.members.add(initial_member)

    @transaction.atomic
    def perform_update(self, serializer: BaseSerializer[StudyGroup]) -> None:
        """
        formdata 의 head_image 가 빈 값이면, 이미지를 삭제하고 빈 값으로 저장합니다.
        """
        assert serializer.instance is not None
        if self.request.data.get("head_image") == "":
            serializer.instance.head_image.delete()
            serializer.instance.head_image = None
        super().perform_update(serializer)

    @extend_schema(summary="스터디그룹 홍보글 목록을 조회합니다.")
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="새로운 스터디그룹을 개설합니다.")
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="특정 스터디그룹 상세 정보를 조회합니다.")
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 정보를 수정합니다.")
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="특정 스터디그룹을 삭제합니다.")
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["스터디그룹 멤버 관리 API"])
class StudyGroupMemberListAPI(generics.ListCreateAPIView):
    permission_classes = (StudyGroupAddMember,)
    queryset = StudyGroupMember.objects.all()
    serializer_class = StudyGroupMemberSchema
    serializer_classes = {
        "GET": StudyGroupMemberSchema,
        "POST": StudyGroupMemberCreateRequestBody,
    }
    filterset_fields = ("is_approved",)

    def get_serializer_class(self) -> type[BaseSerializer[StudyGroupMember]]:
        return self.serializer_classes.get(self.request.method, self.serializer_class)

    def get_queryset(self) -> QuerySet[StudyGroupMember]:
        """
        QueryString 으로 전달받은 uuid 에 해당하는 스터디그룹의 멤버 목록을 조회합니다.
        """
        assert self.kwargs.get("uuid") is not None
        return StudyGroupMember.objects.filter(studygroup__uuid=self.kwargs["uuid"])

    @transaction.atomic
    def perform_create(self, serializer: BaseSerializer[StudyGroupMember]) -> None:
        """
        스터디그룹에 참가를 요청합니다.

        1. 현재 로그인한 유저 식별
        2. 스터디그룹 식별
        3. 스터디그룹에 참가를 요청
        """
        studygroup = StudyGroup.objects.get(uuid=self.kwargs["uuid"])
        new_member = StudyGroupMember.objects.create(
            user=self.request.user,
            studygroup=studygroup,
            request_message=serializer.validated_data.get("request_message"),
        )
        studygroup.members.add(new_member)

    @extend_schema(summary="특정 스터디그룹의 멤버 목록을 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="특정 스터디그룹에 참가를 요청합니다.")
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().post(request, *args, **kwargs)


@extend_schema(tags=["스터디그룹 멤버 관리 API"])
class StudyGroupMemberDetailAPI(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    serializer_class = StudyGroupMemberCreateRequestBody
    serializer_classes = {
        "PATCH": StudyGroupMemberUpdateRequestBody,
    }
    permission_classes = (StudyGroupAddMember,)

    def get_queryset(self) -> QuerySet[StudyGroupMember]:
        assert self.kwargs.get("uuid") is not None
        return StudyGroupMember.objects.filter(studygroup__uuid=self.kwargs["uuid"])

    def get_serializer_class(self) -> type[BaseSerializer[StudyGroupMember]]:
        return self.serializer_classes.get(self.request.method, self.serializer_class)

    @extend_schema(summary="스터디그룹의 참가 신청을 승인합니다.")
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹의 참가신청을 거절하거나, 멤버를 탈퇴시킵니다.")
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["카테고리 API"])
class CategoryListAPI(generics.ListAPIView):
    pagination_class = None
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(summary="카테고리 목록을 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
