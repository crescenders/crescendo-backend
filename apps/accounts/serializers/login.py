from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import serializers


class GoogleLoginSerializer(SocialLoginSerializer):  # type: ignore
    code = None
    id_token = None
    access_token = None
    access = serializers.CharField(
        source="access_token", required=True, allow_blank=False
    )
