from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import (
    OpenedByDeadlineStudyGroupFactory,
    StudyGroupGeneralMemberFactory,
    StudyGroupMemberRequestFactory,
)


class DisapproveStudyGroupMemberRequestTestCase(APITestCase):
    def setUp(self) -> None:
        self.studygroup_for_disapproved = OpenedByDeadlineStudyGroupFactory()
        self.studygroup_member_request_for_disapproved = StudyGroupMemberRequestFactory(
            studygroup=self.studygroup_for_disapproved
        )
        self.some_general_studygroup_member = StudyGroupGeneralMemberFactory(
            studygroup=self.studygroup_for_disapproved
        )

    def test_not_anyone_can_disapprove_studygroup_member(self):
        """
        스터디그룹의 멤버 거절은 로그인하지 않으면 불가능합니다.
        """
        url = reverse(
            "studygroupmember-request-detail",
            kwargs={
                "studygroup_uuid": self.studygroup_for_disapproved.uuid,
                "pk": self.studygroup_member_request_for_disapproved.pk,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401, f"response: {response.data}")

    def test_general_member_cannot_disapprove_studygroup_member(self):
        """
        스터디그룹의 멤버 거절은 로그인했더라도 일반 멤버는 불가능합니다.
        """
        self.client.force_authenticate(user=self.some_general_studygroup_member.user)
        url = reverse(
            "studygroupmember-request-detail",
            kwargs={
                "studygroup_uuid": self.studygroup_for_disapproved.uuid,
                "pk": self.studygroup_member_request_for_disapproved.pk,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, f"response: {response.data}")

    def test_leader_can_disapprove_studygroup_member(self):
        """
        스터디그룹의 멤버 거절은 리더인 경우에만 가능합니다.
        """
        self.client.force_authenticate(
            user=self.studygroup_for_disapproved.leaders[0].user
        )
        url = reverse(
            "studygroupmember-request-detail",
            kwargs={
                "studygroup_uuid": self.studygroup_for_disapproved.uuid,
                "pk": self.studygroup_member_request_for_disapproved.pk,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, f"response: {response.data}")

    def test_after_disapproved_studygroup_member_request_is_disapproved(self):
        """
        스터디그룹의 멤버 거절은 리더인 경우에만 가능합니다.
        """
        self.client.force_authenticate(
            user=self.studygroup_for_disapproved.leaders[0].user
        )
        url = reverse(
            "studygroupmember-request-detail",
            kwargs={
                "studygroup_uuid": self.studygroup_for_disapproved.uuid,
                "pk": self.studygroup_member_request_for_disapproved.pk,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, f"response: {response.data}")
        self.assertEqual(
            self.studygroup_for_disapproved.members.count(),
            2,
            f"response: {response.data}",
        )  # 기존 멤버 2명, 추가되지 않음
        self.assertEqual(
            self.studygroup_for_disapproved.requests.count(),
            1,
            f"response: {response.data}",
        )
        self.studygroup_member_request_for_disapproved.refresh_from_db()
        self.assertFalse(
            self.studygroup_member_request_for_disapproved.is_approved,
            f"response: {response.data}",
        )
        self.assertTrue(
            self.studygroup_member_request_for_disapproved.processed,
            f"response: {response.data}",
        )
