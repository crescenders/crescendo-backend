from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.accounts.models import User


class JWTSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "uuid",
            "email",
            "username",
            "created_at",
            "updated_at",
            "_links",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "email": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def get__links(self, obj) -> list[dict[str, str]]:
        request = self.context["request"]
        links = [
            {
                "rel": "self",
                "href": reverse(
                    "user_profile_uuid", kwargs={"uuid": obj.uuid}, request=request
                ),
            }
        ]
        return links


class GoogleLoginSerializer(SocialLoginSerializer):
    code = None
    id_token = None
    access_token = None
    access = serializers.CharField(
        source="access_token", required=True, allow_blank=False
    )
