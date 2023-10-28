from django.contrib import admin

from apps.studygroup.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin[Category]):
    pass
