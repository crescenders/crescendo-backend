from typing import Any, Sequence

from django.db import transaction
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.studygroup.models import StudyGroup, StudyGroupMember, StudyGroupMemberRequest
from apps.studygroup.permission.studygroup import IsStudygroupLeader, IsStudygroupMember
from apps.studygroup.permissions import StudyGroupAddMember
from apps.studygroup.serializers import (
    StudyGroupMemberReadSerializer,
    StudyGroupMemberRequestCreateSerializer,
    StudyGroupMemberRequestManageSerializer,
    StudyGroupMemberRequestReadSerializer,
)


@extend_schema(tags=["스터디그룹 가입요청 관리 API"])
class StudyGroupMemberRequestListAPI(generics.ListCreateAPIView):
    queryset = StudyGroupMemberRequest.objects.all()
    serializer_classes = {
        "GET": StudyGroupMemberRequestReadSerializer,
        "POST": StudyGroupMemberRequestCreateSerializer,
    }
    permission_classes_mapping = {
        "GET": [IsStudygroupLeader],
        "POST": [IsAuthenticated],
    }

    def get_permissions(self) -> Sequence[BasePermission]:
        return [
            permission()
            for permission in self.permission_classes_mapping.get(
                self.request.method, []
            )
        ]

    def get_queryset(self) -> QuerySet[StudyGroupMemberRequest]:
        return self.queryset.filter(
            studygroup__uuid=self.kwargs["studygroup_uuid"],
            is_approved=False,
            processed=False,
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
        studygroup = StudyGroup.objects.get(uuid=self.kwargs["studygroup_uuid"])
        serializer.save(user=self.request.user, studygroup=studygroup)
        super().perform_create(serializer)


@extend_schema(tags=["스터디그룹 가입요청 관리 API"])
class StudyGroupMemberRequestDetailAPI(
    mixins.DestroyModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = StudyGroupMemberRequest.objects.all()
    permission_classes = (IsStudygroupLeader,)
    serializer_class = StudyGroupMemberRequestManageSerializer

    @extend_schema(
        summary="특정 스터디그룹의 가입 요청을 승인합니다. 해당 스터디그룹의 리더만 가능합니다.", operation_id="approve"
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        스터디그룹 가입 요청을 승인합니다. 해당 요청이 승인되었음이 저장됩니다.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="특정 스터디그룹의 가입 요청을 거절합니다. 해당 스터디그룹의 리더만 가능합니다.", operation_id="reject"
    )
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
        studygroup = StudyGroup.objects.get(uuid=self.kwargs["studygroup_uuid"])
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
    permission_classes = (IsStudygroupMember,)  # 스터디그룹 멤버 조회는 스터디그룹의 가입된 멤버만 조회 가능합니다.
    queryset = StudyGroupMember.objects.all()
    serializer_class = StudyGroupMemberReadSerializer

    def get_queryset(self) -> QuerySet[StudyGroupMember]:
        """
        QueryString 으로 전달받은 uuid 에 해당하는 스터디그룹의 멤버 목록을 조회합니다.
        """
        assert self.kwargs.get("studygroup_uuid") is not None
        return StudyGroupMember.objects.filter(
            studygroup__uuid=self.kwargs["studygroup_uuid"]
        )

    @extend_schema(summary="특정 스터디그룹의 멤버 목록을 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)


@extend_schema(tags=["스터디그룹 멤버 관리 API"])
class StudyGroupMemberDetailAPI(generics.DestroyAPIView):
    serializer_class = StudyGroupMemberReadSerializer
    permission_classes = (StudyGroupAddMember,)

    def get_queryset(self) -> QuerySet[StudyGroupMember]:
        assert self.kwargs.get("studygroup_uuid") is not None
        return StudyGroupMember.objects.filter(
            studygroup__uuid=self.kwargs["studygroup_uuid"]
        )

    @extend_schema(summary="스터디그룹의 멤버를 탈퇴시킵니다.")
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)
