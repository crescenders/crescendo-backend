from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import (
    OpenedByDeadlineStudyGroupFactory,
    StudyGroupGeneralMemberFactory,
    UserFactory,
)


class StudyGroupMemberRequestCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.logged_in_user = UserFactory()
        self.studygroup_for_requested = OpenedByDeadlineStudyGroupFactory()

    def test_not_anyone_can_create_studygroup_member_request(self):
        """
        스터디그룹의 멤버 신청은 로그인하지 않으면 불가능합니다.
        """
        url = reverse(
            "studygroup_member_request",
            kwargs={"uuid": self.studygroup_for_requested.uuid},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_logged_in_user_can_create_studygroup_member_request(self):
        """
        스터디그룹의 멤버 신청은 로그인한 유저만 가능합니다.
        """
        url = reverse(
            "studygroup_member_request",
            kwargs={"uuid": self.studygroup_for_requested.uuid},
        )
        data = {"request_message": "가입 신청합니다."}
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    def test_not_duplicate_member_request(self):
        """
        스터디그룹의 멤버 신청은 중복으로 불가능합니다.
        """
        url = reverse(
            "studygroup_member_request",
            kwargs={"uuid": self.studygroup_for_requested.uuid},
        )
        data = {"request_message": "가입 신청합니다."}
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_already_member_cannot_create_studygroup_member_request(self):
        """
        스터디그룹의 멤버 신청은 이미 가입된 멤버는 불가능합니다.
        """
        already_member = StudyGroupGeneralMemberFactory(
            studygroup=self.studygroup_for_requested
        )
        self.studygroup_for_requested.members.add(already_member)
        self.client.force_authenticate(user=already_member.user)
        url = reverse(
            "studygroup_member_request",
            kwargs={"uuid": self.studygroup_for_requested.uuid},
        )
        data = {"request_message": "가입 신청합니다."}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
