from werkzeug.security import check_password_hash, generate_password_hash

from core.extensions import db
from core.utils.basemodel import BaseModel, TimeStampedMixin, UUIDMixin


class User(BaseModel, TimeStampedMixin, UUIDMixin):
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(10), unique=True)
    first_name = db.Column(db.String(4))
    last_name = db.Column(db.String(4))
    gender = db.Column(db.Enum("남자", "여자"))
    phone_number = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(120))

    def get_full_name(self):
        """성 + 이름"""
        return self.first_name + self.last_name

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<id:{self.id}, full_name:{self.get_full_name()}>"
