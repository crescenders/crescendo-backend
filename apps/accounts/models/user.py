import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AnonymousUser, PermissionsMixin
from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimestampedModel


class UserManager(BaseUserManager["User"]):
    def create_user(
        self, email: str, username: str, password: str | None = None
    ) -> "User":
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, username: str, password: str | None = None
    ) -> "User":
        user: User = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_("email"), unique=True, max_length=80)
    username = models.CharField(_("username"), max_length=64, null=False)
    is_admin = models.BooleanField(_("is_admin"), default=False)

    def __str__(self) -> str:
        return self.email

    def has_perm(
        self, perm: str, obj: Model | Model | AnonymousUser | None = None
    ) -> bool:
        return True

    def has_module_perms(self, app_label: str) -> bool:
        return True

    @property
    def is_staff(self) -> bool:
        return self.is_admin
