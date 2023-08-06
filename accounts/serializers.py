from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import serializers

from accounts.models import User


class JWTSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
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


class GoogleLoginSerializer(SocialLoginSerializer):
    code = None
    id_token = None
    access_token = None
    access = serializers.CharField(
        source="access_token", required=True, allow_blank=False
    )
