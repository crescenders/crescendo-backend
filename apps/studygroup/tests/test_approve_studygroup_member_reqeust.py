from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import (
    OpenedByDeadlineStudyGroupFactory,
    StudyGroupGeneralMemberFactory,
    StudyGroupMemberRequestFactory,
)


class ApproveStudyGroupMemberRequestTestCase(APITestCase):
    def setUp(self) -> None:
        self.studygroup_for_approved = OpenedByDeadlineStudyGroupFactory()
        self.studygroup_member_request_for_approved = StudyGroupMemberRequestFactory(
            studygroup=self.studygroup_for_approved
        )
        self.some_general_studygroup_member = StudyGroupGeneralMemberFactory(
            studygroup=self.studygroup_for_approved
        )

        self.another_studygroup = OpenedByDeadlineStudyGroupFactory()

    def test_not_anyone_can_approve_studygroup_member(self):
        """
        스터디그룹의 멤버 승인은 로그인하지 않으면 불가능합니다.
        """
        url = reverse(
            "studygroup_member_request_detail",
            kwargs={
                "uuid": self.studygroup_for_approved.uuid,
                "pk": self.studygroup_member_request_for_approved.pk,
            },
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401, f"response: {response.data}")

    def test_general_member_cannot_approve_studygroup_member(self):
        """
        스터디그룹의 멤버 승인은 로그인했더라도 일반 멤버는 불가능합니다.
        """
        self.client.force_authenticate(user=self.some_general_studygroup_member.user)
        url = reverse(
            "studygroup_member_request_detail",
            kwargs={
                "uuid": self.studygroup_for_approved.uuid,
                "pk": self.studygroup_member_request_for_approved.pk,
            },
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403, f"response: {response.data}")

    def test_leader_can_approve_studygroup_member(self):
        """
        스터디그룹의 멤버 승인은 리더인 경우에만 가능합니다.
        """
        self.client.force_authenticate(
            user=self.studygroup_for_approved.leaders[0].user
        )
        url = reverse(
            "studygroup_member_request_detail",
            kwargs={
                "uuid": self.studygroup_for_approved.uuid,
                "pk": self.studygroup_member_request_for_approved.pk,
            },
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201), f"response: {response.data}"
        self.assertEqual(
            self.studygroup_for_approved.members.count(),
            3,
            f"response: {response.data}",
        )  # 기존 멤버 2명에, 새로운 멤버 1명

    def another_leader_cannot_approve_studygroup_member(self):
        """
        다른 스터디그룹의 리더는 스터디그룹의 멤버 승인을 할 수 없습니다.
        """
        self.client.force_authenticate(user=self.another_studygroup.leaders[0].user)
        url = reverse(
            "studygroup_member_request_detail",
            kwargs={
                "uuid": self.studygroup_for_approved.uuid,
                "pk": self.studygroup_member_request_for_approved.pk,
            },
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403, f"response: {response.data}")
        self.assertEqual(
            self.studygroup_for_approved.members.count(),
            2,
            f"response: {response.data}",
        )

    def test_after_approve_studygroup_member_request_is_approved_and_processed(self):
        """
        스터디그룹의 멤버 승인이 완료되면, 아래의 과정이 수행되어야 합니다.

        1. 스터디그룹 멤버 요청의 processed 필드가 True 로 변경됩니다.
        2. 스터디그룹 멤버 요청의 is_approved 필드가 True 로 변경됩니다.
        3. 스터디그룹 멤버 요청의 스터디그룹 멤버로서의 생성이 수행됩니다.
        4. 추가된 멤버는 is_leader 필드가 False 로 설정됩니다.
        5. 스터디그룹 요청은 그대로 남아있어야 합니다.
        """

        self.client.force_authenticate(
            user=self.studygroup_for_approved.leaders[0].user
        )
        url = reverse(
            "studygroup_member_request_detail",
            kwargs={
                "uuid": self.studygroup_for_approved.uuid,
                "pk": self.studygroup_member_request_for_approved.pk,
            },
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
        self.assertEqual(
            self.studygroup_for_approved.members.count(),
            3,
            f"response: {response.data}",
        )  # 기존 멤버 2명에, 새로운 멤버 1명

        # 스터디그룹 멤버 요청은 그대로 남아있어야 합니다.
        self.assertEqual(
            self.studygroup_for_approved.requests.count(),
            1,
            f"response: {response.data}",
        )

        # 처리되고 난 후, 요청의 필드들이 "처리됨", "승인됨" 으로 변경되어야 합니다.
        self.studygroup_member_request_for_approved.refresh_from_db()
        self.assertTrue(
            self.studygroup_member_request_for_approved.processed,
            f"response: {response.data}",
        )
        self.assertTrue(
            self.studygroup_member_request_for_approved.is_approved,
            f"response: {response.data}",
        )
