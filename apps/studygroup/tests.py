import random
import uuid
from datetime import timedelta

from django.utils.datetime_safe import date
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.studygroup.models import Category, StudyGroup, StudyGroupMember, Tag


class CategoryTestCase(APITestCase):
    """
    카테고리 API 테스트
    """

    def setUp(self) -> None:
        categories = [Category(name=name) for name in ["백엔드", "프론트엔드", "데브옵스"]]
        Category.objects.bulk_create(categories)

    def test_read_categories(self):
        url = reverse("category_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(
            response.data, [{"name": "백엔드"}, {"name": "프론트엔드"}, {"name": "데브옵스"}]
        )


class StudyGroupReadTestCase(APITestCase):
    def setUp(self):
        # 태그 생성
        tag_names = ["웹 개발", "데이터 분석", "알고리즘", "클라우드", "보안", "인공지능", "머신러닝"]
        tags = [Tag(name=name) for name in tag_names]
        Tag.objects.bulk_create(tags)

        # 카테고리 생성
        categories = [Category(name=name) for name in ["백엔드", "프론트엔드", "데브옵스"]]
        Category.objects.bulk_create(categories)

        # 유저 생성
        users = [
            User(
                email=f"user-{i}@example.com",
                username=f"user-{i}",
                password=f"password-{i}",
            )
            for i in range(30)
        ]
        User.objects.bulk_create(users)

        # 마감된 스터디그룹 생성
        # 모집 완료된 스터디, [오늘 날짜 > deadline]
        django_study = StudyGroup.objects.create(
            name="Django 스터디",
            member_limit=2,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            deadline=date.today() - timedelta(days=1),
            title="Django 스터디 모집합니다.",
            content="Django 는 파이썬 기반의 오픈소스 웹 프레임워크입니다. Django 를 함께 공부하실 분들을 모집합니다.",
        )
        django_leader = StudyGroupMember.objects.create(
            user=User.objects.get(username="user-0"),
            study_group=django_study,
            is_leader=True,
        )
        django_study.members.add(
            django_leader,
        )

        # 모집 완료된 스터디, [현재 인원 == member_limit]
        spring_study = StudyGroup.objects.create(
            name="Spring Boot 스터디",
            member_limit=4,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=7),
            deadline=date.today() + timedelta(days=1),
            title="Spring Boot 스터디 모집합니다.",
            content="Spring Boot 는 스프링 프레임워크를 기반으로 한 Java 기반의 오픈소스 프레임워크입니다."
            + "Spring Boot 를 함께 공부하실 분들을 모집합니다.",
        )
        spring_leader = StudyGroupMember.objects.create(
            user=User.objects.get(username="user-1"),
            study_group=spring_study,
            is_leader=True,
        )
        spring_study.members.add(
            spring_leader,
        )
        # 3명 추가, 총 4명
        for i in range(3):
            member = StudyGroupMember.objects.create(
                user=User.objects.get(username=f"user-{i+2}"),
                study_group=spring_study,
                is_leader=False,
            )
            spring_study.members.add(member)

        # 모집 완료된 스터디, [현재 인원 < member_limit and 오늘 날짜 > deadline]
        react_study = StudyGroup.objects.create(
            name="React 스터디",
            member_limit=5,
            start_date=date.today() + timedelta(days=4),
            end_date=date.today() + timedelta(days=30),
            deadline=date.today() - timedelta(days=1),
            title="React 스터디 모집합니다.",
            content="React 는 페이스북에서 개발한 오픈소스 프론트엔드 라이브러리입니다."
            + "React 를 함께 공부하실 분들을 모집합니다.",
        )
        react_leader = StudyGroupMember.objects.create(
            user=User.objects.get(username="user-2"),
            study_group=react_study,
            is_leader=True,
        )
        react_study.members.add(
            react_leader,
        )

        # add 20 more study groups, which is not completed
        for i in range(20):
            study_group = StudyGroup.objects.create(
                name=f"Study Group {i}",
                member_limit=random.randint(2, 10),
                start_date=date.today() + timedelta(days=random.randint(1, 10)),
                end_date=date.today() + timedelta(days=random.randint(11, 30)),
                deadline=date.today() + timedelta(days=random.randint(1, 10)),
                title=f"Study Group {i} 모집합니다.",
                content=f"Study Group {i} 를 함께 공부하실 분들을 모집합니다.",
            )
            leader = StudyGroupMember.objects.create(
                user=User.objects.get(username=f"user-{i+3}"),
                study_group=study_group,
                is_leader=True,
            )
            study_group.members.add(leader)
            for j in range(random.randint(1, 10)):
                member = StudyGroupMember.objects.create(
                    user=User.objects.get(username=f"user-{i+3+j}"),
                    study_group=study_group,
                    is_leader=False,
                )
                study_group.members.add(member)

    def test_read_studygroup_auth(self):
        """
        스터디그룹 목록 조회는 아무런 인증 정보 없이 할 수 있어야 합니다.
        """
        url = reverse("studygroup_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

    def test_read_studygroup_only_in_progress(self):
        """
        스터디그룹 목록 조회는 진행 중인 스터디그룹만 조회할 수 있어야 합니다.
        모집이 진행 중인 경우는 아래의 두 가지 경우와 같습니다.
        - 오늘 날짜 > deadline
        - 현재 인원 == member_limit
        - 현재 인원 < member_limit and 오늘 날짜 < deadline
        """
        for studygroup in StudyGroup.objects.all():
            print(studygroup, studygroup.is_closed)
