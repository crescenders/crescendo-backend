from typing import Any, Sequence

from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.accounts.models import User
from apps.studygroup.filters import StudyGroupListFilter
from apps.studygroup.models import (
    Category,
    StudyGroup,
    StudyGroupMember,
    StudyGroupMemberRequest,
)
from apps.studygroup.pagination import StudyGroupPagination
from apps.studygroup.permissions import (
    IsStudyGroupLeader,
    StudyGroupAddMember,
    StudyGroupCreatePermission,
    StudyGroupDeleteOrUpdatePermission,
    StudyGroupMemberRead,
)
from apps.studygroup.serializers import (
    CategoryReadSerializer,
    StudyGroupDetailSerializer,
    StudyGroupListSerializer,
    StudyGroupMemberReadSerializer,
    StudyGroupMemberRequestCreateSerializer,
    StudyGroupMemberRequestManageSerializer,
    StudyGroupMemberRequestReadSerializer,
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
    permission_classes = (AllowAny,)
    # Filtering
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StudyGroupListFilter

    # Pagination
    pagination_class = StudyGroupPagination

    def get_permissions(self) -> Sequence[BasePermission]:
        """
        스터디그룹을 생성할 때, 스터디그룹장이 되는 유저는 스터디그룹장 권한을 가지고 있어야 합니다.
        """
        if self.action == "create":
            return [permission() for permission in [StudyGroupCreatePermission]]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permission() for permission in [StudyGroupDeleteOrUpdatePermission]]
        return super().get_permissions()

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


@extend_schema(tags=["스터디그룹 가입요청 관리 API"])
class StudyGroupMemberRequestListAPI(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StudyGroupMemberRequestCreateSerializer
    queryset = StudyGroupMemberRequest.objects.all()
    serializer_classes = {
        "GET": StudyGroupMemberRequestReadSerializer,
        "POST": StudyGroupMemberRequestCreateSerializer,
    }

    def get_permissions(self) -> Sequence[BasePermission]:
        if self.request.method == "GET":
            return [permission() for permission in [IsStudyGroupLeader]]
        elif self.request.method == "POST":
            return [permission() for permission in [IsAuthenticated]]
        return super().get_permissions()

    def get_queryset(self) -> QuerySet[StudyGroupMemberRequest]:
        return self.queryset.filter(
            studygroup__uuid=self.kwargs["uuid"], is_approved=False, processed=False
        )

    def get_serializer_class(self) -> type[BaseSerializer[StudyGroupMemberRequest]]:
        return self.serializer_classes.get(self.request.method)

    @extend_schema(summary="특정 스터디그룹의 가입 요청 목록을 조회합니다. 해당 스터디그룹의 리더만 가능합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="특정 스터디그룹에 가입 요청을 보냅니다. 누구나 요청을 보낼 수 있습니다.")
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    def perform_create(
        self, serializer: BaseSerializer[StudyGroupMemberRequest]
    ) -> None:
        """
        스터디그룹 가입 요청을 생성합니다.
        """
        studygroup = StudyGroup.objects.get(uuid=self.kwargs["uuid"])
        serializer.save(user=self.request.user, studygroup=studygroup)
        super().perform_create(serializer)


@extend_schema(tags=["스터디그룹 가입요청 관리 API"])
class StudyGroupMemberRequestDetailAPI(
    mixins.DestroyModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = StudyGroupMemberRequest.objects.all()
    permission_classes = (IsStudyGroupLeader,)
    serializer_class = StudyGroupMemberRequestManageSerializer

    @extend_schema(summary="특정 스터디그룹의 가입 요청을 승인합니다. 해당 스터디그룹의 리더만 가능합니다.")
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        스터디그룹 가입 요청을 승인합니다. 해당 요청이 승인되었음이 저장됩니다.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="특정 스터디그룹의 가입 요청을 거절합니다. 해당 스터디그룹의 리더만 가능합니다.")
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        soft delete 를 합니다. 해당 요청이 거절되었음이 저장됩니다.
        """
        return super().destroy(request, *args, **kwargs)

    @transaction.atomic
    def perform_create(
        self, serializer: BaseSerializer[StudyGroupMemberRequest]
    ) -> None:
        """
        스터디그룹 가입 요청을 승인합니다.
        1. 해당 요청이 승인되고, 처리되었음이 저장됩니다.
        2. 스터디그룹의 멤버로 등록됩니다.
        """
        studygroup = StudyGroup.objects.get(uuid=self.kwargs["uuid"])
        studygroup_request = StudyGroupMemberRequest.objects.get(pk=self.kwargs["pk"])
        studygroup_request.is_approved = True
        studygroup_request.processed = True
        studygroup_request.save()
        StudyGroupMember.objects.create(
            user=studygroup_request.user, studygroup=studygroup, is_leader=False
        )

    @transaction.atomic
    def perform_destroy(self, instance: StudyGroupMemberRequest) -> None:
        """
        스터디그룹 가입 요청을 거절합니다.
        1. 해당 요청이 거절되고, 처리되었음이 저장됩니다.
        """
        instance.processed = True
        instance.save()


@extend_schema(tags=["스터디그룹 멤버 관리 API"])
class StudyGroupMemberListAPI(generics.ListAPIView):
    permission_classes = (
        StudyGroupMemberRead,
    )  # 스터디그룹 멤버 조회는 스터디그룹의 가입된 멤버만 조회 가능합니다.
    queryset = StudyGroupMember.objects.all()
    serializer_class = StudyGroupMemberReadSerializer

    def get_queryset(self) -> QuerySet[StudyGroupMember]:
        """
        QueryString 으로 전달받은 uuid 에 해당하는 스터디그룹의 멤버 목록을 조회합니다.
        """
        assert self.kwargs.get("uuid") is not None
        return StudyGroupMember.objects.filter(studygroup__uuid=self.kwargs["uuid"])

    @extend_schema(summary="특정 스터디그룹의 멤버 목록을 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)


@extend_schema(tags=["스터디그룹 멤버 관리 API"])
class StudyGroupMemberDetailAPI(generics.DestroyAPIView):
    serializer_class = StudyGroupMemberReadSerializer
    permission_classes = (StudyGroupAddMember,)

    def get_queryset(self) -> QuerySet[StudyGroupMember]:
        assert self.kwargs.get("uuid") is not None
        return StudyGroupMember.objects.filter(studygroup__uuid=self.kwargs["uuid"])

    @extend_schema(summary="스터디그룹의 멤버를 탈퇴시킵니다.")
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["카테고리 API"])
class CategoryListAPI(generics.ListAPIView):
    pagination_class = None
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer

    @extend_schema(summary="카테고리 목록을 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
