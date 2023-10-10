from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.models import StudyGroup
from apps.studygroup.tests.factories import (
    OpenedByDeadlineStudyGroupFactory,
    StudyGroupGeneralMemberFactory,
)


class DeleteStudyGroupTestCase(APITestCase):
    def setUp(self) -> None:
        self.studygroup_be_deleted = OpenedByDeadlineStudyGroupFactory()
        self.studygroup_member = StudyGroupGeneralMemberFactory(
            studygroup=self.studygroup_be_deleted
        )

    def test_not_logged_in_user_cannot_delete_studygroup(self):
        """
        스터디그룹 삭제는 로그인하지 않으면 불가능합니다.
        """
        url = reverse(
            "studygroup_detail", kwargs={"uuid": self.studygroup_be_deleted.uuid}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_general_member_cannot_delete_studygroup(self):
        """
        일반 멤버는 스터디그룹을 삭제할 수 없습니다.
        """
        url = reverse(
            "studygroup_detail", kwargs={"uuid": self.studygroup_be_deleted.uuid}
        )
        self.client.force_authenticate(user=self.studygroup_member.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_only_leader_can_delete_studygroup(self):
        """
        리더만 스터디그룹을 삭제할 수 있습니다.
        """
        url = reverse(
            "studygroup_detail", kwargs={"uuid": self.studygroup_be_deleted.uuid}
        )
        self.client.force_authenticate(user=self.studygroup_be_deleted.leaders[0].user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(StudyGroup.objects.count(), 0)
