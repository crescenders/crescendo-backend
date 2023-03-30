from crescendo.users.models import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash


class UserService:
    """회원정보조회, 회원가입, 회원정보수정, 회원탈퇴, 검색"""

    def create_user(self, **kwargs):
        """사용자를 한 명 생성합니다.
        비밀번호는 암호화되어 저장됩니다."""
        kwargs.update({"password": generate_password_hash(kwargs.get("password"))})

    def get_all_users(self, **kwargs):
        """모든 사용자 리스트를 반환합니다."""
        return User.query.all()

    def get_one_user(self, uuid):
        """한 명의 사용자 인스턴스를 반환합니다."""

    def update_user(self):
        """사용자를 특정하여 회원정보를 수정합니다."""

    def withdraw(self, uuid):
        """사용자를 특정하여 회원탈퇴를 진행합니다."""
