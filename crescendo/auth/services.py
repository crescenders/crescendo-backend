from abc import ABC, abstractmethod
from typing import Optional

from fullask_rest_framework.entities.pagination import PaginationResponse
from google.auth.transport import requests  # type: ignore[import]
from google.oauth2 import id_token  # type: ignore[import]

from crescendo.auth.entities import JWTResponse, UserEntity
from crescendo.auth.repositories import FullUserRepositoryABC


class UserServiceABC(ABC):
    @abstractmethod
    def get_list(
        self,
        pagination_request,
        sorting_request,
        filtering_request,
    ) -> PaginationResponse[UserEntity]:
        pass

    @abstractmethod
    def get_one(self, user_uuid) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def edit_info(self, user_uuid: str, data) -> UserEntity:
        pass

    @abstractmethod
    def withdraw(self, user_uuid) -> None:
        pass

    @abstractmethod
    def google_login(self, data) -> JWTResponse:
        """
        Google 인증 서버를 이용해 회원가입 및 로그인을 진행합니다.
        이미 가입되어 있는 회원의 경우 토큽 발급만,
        신규 회원인 경우 회원가입 후 토큰 발급을 처리합니다.
        """
        pass

    @abstractmethod
    def refresh_login(self, decoded_refresh_token) -> JWTResponse:
        pass


class UserService(UserServiceABC):
    """회원정보조회, 회원가입, 회원정보수정, 회원탈퇴, 검색"""

    def __init__(
        self,
        user_repository: FullUserRepositoryABC,
        user_entity: UserEntity,
    ):
        self.user_repository = user_repository
        self.user_entity = user_entity

    def get_list(
        self,
        pagination_request,
        sorting_request,
        filtering_request,
    ) -> PaginationResponse[UserEntity]:
        return self.user_repository.read_all_with_pagination(
            pagination_request=pagination_request,
            sorting_request=sorting_request,
            filtering_request=filtering_request,
        )

    def get_one(self, user_uuid) -> Optional[UserEntity]:
        return self.user_repository.read_by_uuid(uuid=user_uuid)

    def edit_info(self, user_uuid: str, data) -> UserEntity:
        user = self.user_repository.read_by_uuid(uuid=user_uuid)
        user.username = data["username"]
        return self.user_repository.save(user)

    def withdraw(self, user_uuid) -> None:
        user = self.user_repository.read_by_uuid(uuid=user_uuid)
        return self.user_repository.delete(user)

    def google_login(self, data) -> JWTResponse:
        id_information = id_token.verify_oauth2_token(data, requests.Request())
        email = id_information["email"]
        username = id_information["given_name"]

        user = (
            self.user_repository.read_by_email(email)
            if self.user_repository.read_by_email(email)
            else self._register(email, username)
        )

        return JWTResponse(
            access_token=user.access_token, refresh_token=user.refresh_token
        )

    def refresh_login(self, decoded_refresh_token) -> JWTResponse:
        user = self.user_repository.read_by_uuid(decoded_refresh_token["sub"])
        return JWTResponse(
            access_token=user.access_token, refresh_token=user.refresh_token
        )

    def _register(self, email, username, role="USER") -> UserEntity:
        user = UserEntity(email=email, username=username, role=role)
        return self.user_repository.save(user)
