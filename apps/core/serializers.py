from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from rest_framework import serializers


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data: Any) -> Model:
        try:
            result = self.get_queryset().get(**{str(self.slug_field): data})
            assert isinstance(result, Model)
            return result
        except ObjectDoesNotExist:
            result = self.get_queryset().create(**{str(self.slug_field): data})
            assert isinstance(result, Model)
            return result
        except (TypeError, ValueError):
            self.fail("invalid")
