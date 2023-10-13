from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import (
    OpenedByDeadlineStudyGroupFactory,
    StudyGroupGeneralMemberFactory,
    StudyGroupMemberRequestFactory,
)

MEMBER_REQUEST_FORMAT_KEYS = {
    "id",
    "user",
    "request_message",
}

USER_FORMAT_KEYS = {
    "uuid",
    "email",
    "username",
    "created_at",
    "updated_at",
}


class StudyGroupMemberRequestReadListTestCase(APITestCase):
    def setUp(self) -> None:
        self.studygroup_for_requested = OpenedByDeadlineStudyGroupFactory()
        self.some_general_studygroup_member = StudyGroupGeneralMemberFactory(
            studygroup=self.studygroup_for_requested
        )
        # 3개의 멤버 신청을 생성합니다.
        StudyGroupMemberRequestFactory.create_batch(
            3, studygroup=self.studygroup_for_requested
        )
        # 1개의 승인된 신청을 생성합니다.
        StudyGroupMemberRequestFactory(
            studygroup=self.studygroup_for_requested, is_approved=True, processed=True
        )
        # 1개의 거절된 신청을 생성합니다.
        StudyGroupMemberRequestFactory(
            studygroup=self.studygroup_for_requested, is_approved=False, processed=True
        )

    def test_not_logged_in_user_cannot_read_studygroup_member_request_list(self):
        """
        스터디그룹의 멤버 신청 목록 조회는 로그인하지 않으면 불가능합니다.
        """
        url = reverse(
            "studygroup_member_request_list",
            kwargs={"uuid": self.studygroup_for_requested.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401, f"response: {response.data}")

    def test_general_member_cannot_read_studygroup_member_request_list(self):
        """
        스터디그룹의 멤버 신청 목록 조회는 로그인했더라도 일반 멤버는 불가능합니다.
        """
        self.client.force_authenticate(user=self.some_general_studygroup_member.user)
        url = reverse(
            "studygroup_member_request_list",
            kwargs={"uuid": self.studygroup_for_requested.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403, f"response: {response.data}")

    def test_leader_can_read_studygroup_member_request_list(self):
        """
        스터디그룹의 멤버 신청 목록 조회는 리더인 경우에만 가능합니다.
        """
        self.client.force_authenticate(
            user=self.studygroup_for_requested.leaders[0].user
        )
        url = reverse(
            "studygroup_member_request_list",
            kwargs={"uuid": self.studygroup_for_requested.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"response: {response.data}")

    def test_only_returns_unprocessed_and_disapproved_requests(self):
        """
        스터디그룹의 멤버 신청 목록 조회는 처리되지 않고 아직 거절된 신청만 반환해야 합니다.
        """
        self.client.force_authenticate(
            user=self.studygroup_for_requested.leaders[0].user
        )
        url = reverse(
            "studygroup_member_request_list",
            kwargs={"uuid": self.studygroup_for_requested.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"response: {response.data}")
        self.assertEqual(len(response.data), 3, f"response: {response.data}")

    def test_read_studygroup_member_request_list_format(self):
        """
        스터디그룹의 멤버 신청 목록 조회의 응답 포맷을 확인합니다.
        """
        self.client.force_authenticate(
            user=self.studygroup_for_requested.leaders[0].user
        )
        url = reverse(
            "studygroup_member_request_list",
            kwargs={"uuid": self.studygroup_for_requested.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"response: {response.data}")
        for item in response.data:
            self.assertEqual(
                set(item.keys()),
                MEMBER_REQUEST_FORMAT_KEYS,
                f"response: {response.data}",
            )
            self.assertEqual(
                set(item["user"].keys()), USER_FORMAT_KEYS, f"response: {response.data}"
            )
