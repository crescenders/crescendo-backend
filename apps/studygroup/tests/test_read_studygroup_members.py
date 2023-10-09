from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import (
    OpenedByDeadlineStudyGroupFactory,
    StudyGroupGeneralMemberFactory,
)

MEMBER_LIST_FORMAT_KEYS = {
    "id",
    "user",
    "is_leader",
    "created_at",
}

USER_FORMAT_KEYS = {
    "uuid",
    "email",
    "username",
    "created_at",
    "updated_at",
}


class StudyGroupMemberReadTestCase(APITestCase):
    def setUp(self) -> None:
        self.studygroup_for_read = OpenedByDeadlineStudyGroupFactory()
        self.general_member = StudyGroupGeneralMemberFactory(
            studygroup=self.studygroup_for_read
        )
        self.studygroup_for_read.members.add(self.general_member)

        self.another_studygroup = OpenedByDeadlineStudyGroupFactory()
        self.another_general_member = StudyGroupGeneralMemberFactory(
            studygroup=self.another_studygroup
        )
        self.another_studygroup.members.add(self.another_general_member)

    def test_not_anyone_can_read_studygroup_member(self):
        """
        스터디그룹의 멤버 조회는 로그인하지 않으면 불가능합니다.
        """
        url = reverse(
            "studygroup_members", kwargs={"uuid": self.studygroup_for_read.uuid}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_member_can_read_studygroup_member(self):
        """
        스터디그룹의 멤버 조회는 스터디에 가입된 멤버만 가능합니다.
        """
        url = reverse(
            "studygroup_members", kwargs={"uuid": self.studygroup_for_read.uuid}
        )
        self.client.force_authenticate(user=self.general_member.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_leader_can_read_studygroup_member(self):
        """
        스터디그룹장은 스터디그룹의 멤버를 조회할 수 있습니다.
        """
        url = reverse(
            "studygroup_members", kwargs={"uuid": self.studygroup_for_read.uuid}
        )
        self.client.force_authenticate(user=self.studygroup_for_read.leaders[0].user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # 위의 테스트코드가 성공했다고 가정하고 진행합니다.
    def test_studygroup_member_response_format(self):
        """
        스터디그룹의 멤버 조회의 포맷을 검증합니다.
        """
        url = reverse(
            "studygroup_members", kwargs={"uuid": self.studygroup_for_read.uuid}
        )
        self.client.force_authenticate(user=self.general_member.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.data[0].keys()),
            MEMBER_LIST_FORMAT_KEYS,
        )
        self.assertEqual(
            set(response.data[0]["user"].keys()),
            USER_FORMAT_KEYS,
        )

    def test_another_general_member_cannot_read_studygroup_member(self):
        """
        다른 스터디그룹에 가입된 일반 멤버는 스터디그룹의 멤버를 조회할 수 없습니다.
        """
        url = reverse(
            "studygroup_members", kwargs={"uuid": self.studygroup_for_read.uuid}
        )
        self.client.force_authenticate(user=self.another_general_member.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_another_leader_member_cannot_read_studygroup_member(self):
        """
        다른 스터디그룹의 리더는 스터디그룹의 멤버를 조회할 수 없습니다.
        """
        url = reverse(
            "studygroup_members", kwargs={"uuid": self.studygroup_for_read.uuid}
        )
        self.client.force_authenticate(user=self.another_studygroup.leaders[0].user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
