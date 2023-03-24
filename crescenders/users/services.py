from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from crescenders.users.repositories import UserRepository


class UserService:
    """회원정보조회, 회원가입, 회원정보수정, 회원탈퇴, 검색"""

    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, **kwargs):
        """사용자를 한 명 생성합니다.
        비밀번호는 암호화되어 저장됩니다."""
        kwargs.update({"password": generate_password_hash(kwargs.get("password"))})
        return self.repository.create(**kwargs)

    def get_all_users(self, **kwargs):
        """모든 사용자 리스트를 반환합니다."""
        return self.repository.get_all(**kwargs)

    def get_one_user(self, uuid):
        """한 명의 사용자 인스턴스를 반환합니다."""
        return self.repository.read_by_uuid(uuid)

    def update_user(self):
        """사용자를 특정하여 회원정보를 수정합니다."""
        return self.repository.update()

    def withdraw(self, uuid):
        """사용자를 특정하여 회원탈퇴를 진행합니다."""
        return self.get_one_user(uuid=uuid).delete()
