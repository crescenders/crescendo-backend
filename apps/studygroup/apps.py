from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StudygroupConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.studygroup"
    verbose_name = _("StudyGroup")
