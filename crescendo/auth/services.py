from abc import ABC, abstractmethod
from typing import Optional

from google.auth.transport import requests  # type: ignore[import]
from google.oauth2 import id_token  # type: ignore[import]

from core.entities.pagination import PaginationEntity
from crescendo.auth.entities import UserEntity
from crescendo.auth.repositories import UserRepositoryABC


class UserServiceABC(ABC):
    @abstractmethod
    def get_list(
        self,
        page: int,
        per_page: int,
        filter_by: Optional[str],
        ordering: str,
    ) -> PaginationEntity[UserEntity]:
        """
        페이지네이션, 필터링, 정렬조건을 적용하여 사용자의 목록을 반환합니다.

        :param page: 페이지 숫자
        :param per_page: 페이지당 보여줄 아이템 갯수
        :param filter_by: 검색어
        :param ordering: 정렬 조건
        :return: 페이지네이션 처리된 사용자 엔티티 목록
        """
        pass

    @abstractmethod
    def get_one(self, uuid) -> UserEntity:
        pass

    @abstractmethod
    def edit_info(self, uuid: str, data) -> UserEntity:
        pass

    @abstractmethod
    def withdraw(self, uuid) -> None:
        pass

    @abstractmethod
    def oauth2_login(self, oauth2_provider: str, data) -> dict:
        """
        외부 인증 서버(Google, Kakao, Github 등) 을 이용한 Oauth2 로그인을 진행합니다.

        :param oauth2_provider: 외부 인증 서버의 종류
        :param data: jwt, 인가 토큰 등 외부 서버에서 발급받은 토큰
        """
        pass


class UserService(UserServiceABC):
    """회원정보조회, 회원가입, 회원정보수정, 회원탈퇴, 검색"""

    def __init__(self, user_repository: UserRepositoryABC, user_entity_cls: UserEntity):
        self.user_repository = user_repository
        self.user_entity_cls = user_entity_cls

    def get_list(
        self,
        page: int,
        per_page: int,
        filter_by: Optional[str],
        ordering: str,
    ) -> PaginationEntity[UserEntity]:
        return self.user_repository.read_list(
            page=page, per_page=per_page, filter_by=filter_by, ordering=ordering
        )

    def get_one(self, uuid) -> UserEntity:
        return self.user_repository.read_one_by_uuid(uuid=uuid)

    def edit_info(self, uuid: str, data) -> UserEntity:
        pass

    def withdraw(self, uuid) -> None:
        pass

    def oauth2_login(self, oauth2_provider: str, data) -> dict:
        """
        외부 인증 서버(Google, Kakao, Github 등) 을 이용한 Oauth2 로그인을 진행합니다.

        사용자를 저장하기 위해서는 필히 아래의 정보들이 필요합니다.

        - email
        - username

        :param oauth2_provider: 외부 인증 서버의 종류
        :param data: jwt, 인가 토큰 등 외부 서버에서 발급받은 토큰
        """
        if oauth2_provider == "google":
            pass

        elif oauth2_provider == "kakao":
            pass
        return {"email": "", "username": ""}

    def _google_oauth2_login(self, data):
        # Google JWT 검증
        frontend_google_client_id = (
            "560831292125-jnlpjp0chs024i3p8hn7ifr7uidigqok.apps.googleusercontent.com"
        )
        id_information = id_token.verify_oauth2_token(data, requests.Request())
        email = id_information["email"]
        username = id_information["given_name"]

    def _check_user_exists(self, email) -> Optional[UserEntity]:
        """
        repository 에서 사용자가 존재하는지 체크하고, 존재한다면 UserEntity 객체를, 그렇지 않다면 None을 반환합니다.

        :param email: 사용자의 이메일
        :return: UserEntity or None
        """
        current_user = self.user_repository.read_one_by_email(email=email)
        return current_user

    def _entity_to_model(self, entity):
        pass

    def _model_to_entity(self, model):
        pass
