from flask_jwt_extended import create_access_token, create_refresh_token


class UserEntity:
    def __init__(self, email: str, role: str, username: str):
        self.email = email
        self.role = role
        self.username = username

    def create_access_token(self):
        pass

    def create_refresh_token(self):
        pass
