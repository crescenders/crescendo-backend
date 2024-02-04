from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import (
    AssignmentRequestFactory,
    ClosedByDeadlineStudyGroupFactory,
    StudyGroupGeneralMemberFactory,
)


class AssignmentListTestCase(APITestCase):
    """
    과제 목록 조회 API 테스트
    """

    def setUp(self) -> None:
        self.studygroup = ClosedByDeadlineStudyGroupFactory()
        self.studygroup_member = StudyGroupGeneralMemberFactory(
            studygroup=self.studygroup
        )
        self.assignment_requests = AssignmentRequestFactory.create_batch(
            3,
            studygroup=self.studygroup,
            author=self.studygroup.leaders[0],
        )

    def test_not_logged_in_user_cannot_read_assignment_list(self):
        """
        과제 목록 조회는 로그인하지 않아도 할 수 있습니다.
        """
        url = reverse(
            "assignment-request-list",
            kwargs={"studygroup_uuid": self.studygroup.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"response: {response.data}")

    def test_not_logged_in_user_can_read_only_assignment_title(self):
        """
        과제 목록 조회는 로그인하지 않아도 할 수 있지만, 과제 제목만 볼 수 있습니다.
        """
        url = reverse(
            "assignment-request-list",
            kwargs={"studygroup_uuid": self.studygroup.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            f"response: {response.data}",
        )
        self.assertEqual(
            len(response.data["results"]),
            3,
            f"response: {response.data}",
        )
        self.assertIn(
            "title", response.data["results"][0]
        ), f"response: {response.data}"
        self.assertIsNotNone(
            response.data["results"][0]["title"]
        ), f"response: {response.data}"
        self.assertEquals(
            response.data["results"][0]["content"], ""
        ), f"response: {response.data}"

    def test_studygroup_member_can_read_assignment_list(self):
        """
        스터디그룹 멤버는 제목과 내용을 볼 수 있습니다.
        """
        url = reverse(
            "assignment-request-list",
            kwargs={"studygroup_uuid": self.studygroup.uuid},
        )
        self.client.force_authenticate(user=self.studygroup_member.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"response: {response.data}")
        self.assertEqual(
            len(response.data["results"]),
            3,
            f"response: {response.data}",
        )
        self.assertIn(
            "title", response.data["results"][0]
        ), f"response: {response.data}"
        self.assertIsNotNone(
            response.data["results"][0]["title"]
        ), f"response: {response.data}"
        self.assertIn(
            "content", response.data["results"][0]
        ), f"response: {response.data}"
        self.assertIsNotNone(
            response.data["results"][0]["content"]
        ), f"response: {response.data}"

    def test_studygroup_member_can_truncated_assignment_content(self):
        """
        스터디그룹 멤버는 기본 값 20글자로 잘린 과제의 내용을 볼 수 있습니다.
        "..." 이 붙어, 총 23글자가 되어야 합니다.
        """
        url = reverse(
            "assignment-request-list",
            kwargs={"studygroup_uuid": self.studygroup.uuid},
        )
        self.client.force_authenticate(user=self.studygroup_member.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"response: {response.data}")
        self.assertEqual(
            len(response.data["results"]),
            3,
            f"response: {response.data}",
        )
        self.assertIn(
            "content", response.data["results"][0]
        ), f"response: {response.data}"
        self.assertTrue(
            all(len(result["content"]) <= 23 for result in response.data["results"])
        )

    def test_studygroup_member_can_truncated_assignment_request_with_custom_count(
        self,
    ):
        """
        스터디그룹 멤버는 과제의 내용을 150자 이내에서 원하는 만큼 잘라 볼 수 있습니다.
        "..." 포함, 내용은 최대 153자가 되어야 합니다.
        """
        url = reverse(
            "assignment-request-list",
            kwargs={"studygroup_uuid": self.studygroup.uuid},
        )
        self.client.force_authenticate(user=self.studygroup_member.user)
        response = self.client.get(url, {"truncate": 150})
        self.assertEqual(response.status_code, 200, f"response: {response.data}")
        self.assertEqual(
            len(response.data["results"]),
            3,
            f"response: {response.data}",
        )
        self.assertIn(
            "content", response.data["results"][0]
        ), f"response: {response.data}"
        self.assertTrue(
            all(len(result["content"]) <= 153 for result in response.data["results"])
        )

    def test_studygroup_member_cannot_read_truncated_assignment_over_150(self):
        """
        스터디그룹 멤버는 과제의 내용을 150자 이상으로 잘라 볼 수 없습니다.
        """
        url = reverse(
            "assignment-request-list",
            kwargs={"studygroup_uuid": self.studygroup.uuid},
        )
        self.client.force_authenticate(user=self.studygroup_member.user)
        response = self.client.get(url, {"truncate": 151})
        self.assertEqual(response.status_code, 400, f"response: {response.data}")

    def test_truncate_must_integer_not_string(self):
        """
        truncate는 숫자여야 합니다.
        """
        url = reverse(
            "assignment-request-list",
            kwargs={"studygroup_uuid": self.studygroup.uuid},
        )
        self.client.force_authenticate(user=self.studygroup_member.user)
        response = self.client.get(url, {"truncate": "string"})
        self.assertEqual(response.status_code, 400, f"response: {response.data}")

    def test_truncate_must_integer_not_float(self):
        """
        truncate는 숫자여야 합니다.
        """
        url = reverse(
            "assignment-request-list",
            kwargs={"studygroup_uuid": self.studygroup.uuid},
        )
        self.client.force_authenticate(user=self.studygroup_member.user)
        response = self.client.get(url, {"truncate": 133.5})
        self.assertEqual(response.status_code, 400, f"response: {response.data}")
