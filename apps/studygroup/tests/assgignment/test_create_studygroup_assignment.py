from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import (
    ClosedByDeadlineStudyGroupFactory,
    StudyGroupGeneralMemberFactory,
)


class AssignmentCreateTestCase(APITestCase):
    """
    과제 요청 생성 API 테스트
    """

    def setUp(self) -> None:
        self.studygroup = ClosedByDeadlineStudyGroupFactory()
        self.studygroup_member = StudyGroupGeneralMemberFactory(
            studygroup=self.studygroup
        )

    def test_not_logged_in_user_cannot_create_assignment(self):
        """
        과제 요청 생성은 로그인하지 않으면 할 수 없습니다.
        """
        url = reverse(
            "assignment-request-list",
            kwargs={"studygroup_uuid": self.studygroup.uuid},
        )
        data = {
            "studygroup": self.studygroup.uuid,
            "title": "test title",
            "content": "test content",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401, f"response: {response.data}")

    def test_only_leader_can_create_assignment(self):
        """
        과제 요청 생성은 리더만 할 수 있습니다.
        """
        self.client.force_authenticate(self.studygroup.leaders[0].user)
        url = reverse(
            "assignment-request-list",
            kwargs={"studygroup_uuid": self.studygroup.uuid},
        )
        data = {
            "studygroup": self.studygroup.uuid,
            "title": "test title",
            "content": "test content",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
