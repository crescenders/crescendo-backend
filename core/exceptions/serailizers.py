from rest_framework import exceptions, serializers
from rest_framework_simplejwt.exceptions import InvalidToken


class BaseExceptionSerializer(serializers.Serializer):
    exception_class = exceptions.APIException

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code"].default = self.exception_class.default_code
        self.fields["detail"].default = self.exception_class.default_detail

    code = serializers.CharField()
    detail = serializers.CharField()


class InvalidTokenExceptionSerializer(BaseExceptionSerializer):
    exception_class = InvalidToken
