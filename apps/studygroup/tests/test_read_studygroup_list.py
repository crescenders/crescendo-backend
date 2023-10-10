from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import OpenedByDeadlineStudyGroupFactory

PAGINATION_LIST_FORMAT_KEYS = {
    "next",
    "previous",
    "results",
}
STUDYGROUP_FORMAT_KEYS = {
    "uuid",
    "head_image",
    "leaders",
    "post_title",
    "study_name",
    "until_deadline",
    "is_closed",
    "tags",
    "categories",
    "current_member_count",
    "member_limit",
}
LEADERS_FORMAT_KEYS = {
    "uuid",
    "username",
    "email",
}


class StudyGroupListTestCase(APITestCase):
    """
    스터디그룹 목록 조회 API 테스트
    """

    @classmethod
    def setUpTestData(cls) -> None:
        # 스터디그룹 10개 생성
        OpenedByDeadlineStudyGroupFactory.create_batch(10)

    def test_read_list_format(self):
        url = reverse("studygroup_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # response.data 의 키들을 확인한다.
        self.assertEqual(set(response.data.keys()), PAGINATION_LIST_FORMAT_KEYS)
        # response.data["results"] 의 각 아이템들의 키들을 확인한다.
        for item in response.data["results"]:
            self.assertEqual(set(item.keys()), STUDYGROUP_FORMAT_KEYS)
            # response.data["results"] 의 각 아이템들의 "leaders" 의 각 아이템들의 키들을 확인한다.
            for leader in item["leaders"]:
                self.assertEqual(set(leader.keys()), LEADERS_FORMAT_KEYS)
