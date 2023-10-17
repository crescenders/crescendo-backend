from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import (
    OpenedByDeadlineStudyGroupFactory,
    StudyGroupMemberRequestFactory,
    UserFactory,
)


class StudyGroupMemberDisapproveTestCase(APITestCase):
    def setUp(self) -> None:
        self.logged_in_user = UserFactory()
        self.studygroup_for_disapproved = OpenedByDeadlineStudyGroupFactory()
        self.studygroup_member_request_for_disapproved = StudyGroupMemberRequestFactory(
            studygroup=self.studygroup_for_disapproved
        )

    def test_not_anyone_can_disapprove_studygroup_member(self):
        """
        스터디그룹의 멤버 거절은 로그인하지 않으면 불가능합니다.
        """
        url = reverse(
            "studygroupmember-request-detail",
            kwargs={
                "uuid": self.studygroup_for_disapproved.uuid,
                "pk": self.studygroup_member_request_for_disapproved.pk,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401, f"response: {response.data}")
