from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import serializers

from apps.accounts.models import User


class JWTSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            "uuid",
            "email",
            "username",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "email": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class GoogleLoginSerializer(SocialLoginSerializer):  # type: ignore
    code = None
    id_token = None
    access_token = None
    access = serializers.CharField(
        source="access_token", required=True, allow_blank=False
    )
