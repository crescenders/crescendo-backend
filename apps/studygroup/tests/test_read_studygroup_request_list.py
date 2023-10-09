from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import (
    OpenedByDeadlineStudyGroupFactory,
    StudyGroupGeneralMemberFactory,
    StudyGroupMemberRequestFactory,
)


class StudyGroupMemberRequestReadListTestCase(APITestCase):
    def setUp(self) -> None:
        self.studygroup_for_requested = OpenedByDeadlineStudyGroupFactory()
        self.some_general_studygroup_member = StudyGroupGeneralMemberFactory(
            studygroup=self.studygroup_for_requested
        )
        StudyGroupMemberRequestFactory.create_batch(
            3, studygroup=self.studygroup_for_requested
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
        self.assertEqual(response.status_code, 401)

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
        self.assertEqual(response.status_code, 403)

    def test_leader_can_read_studygroup_member_request_list(self):
        """
        스터디그룹의 멤버 신청 목록 조회는 리더인 경우에만 가능합니다.
        """
        self.client.force_authenticate(user=self.studygroup_for_requested.leader.user)
        url = reverse(
            "studygroup_member_request_list",
            kwargs={"uuid": self.studygroup_for_requested.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
