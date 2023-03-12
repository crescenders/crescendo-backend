from werkzeug.security import check_password_hash, generate_password_hash

from core.utils.service.baseservice import BaseModelService


class UserService(BaseModelService):
    """회원정보조회, 회원가입, 회원정보수정, 회원탈퇴, 검색"""

    def set_password(self, password):
        self.model.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.model.password, password)
