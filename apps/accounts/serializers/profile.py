from rest_framework import serializers

from apps.accounts.models import User


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
