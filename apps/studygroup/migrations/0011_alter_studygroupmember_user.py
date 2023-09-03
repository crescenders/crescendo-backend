# Generated by Django 4.2.4 on 2023-08-24 18:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("studygroup", "0010_alter_studygroupmember_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studygroupmember",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="study_group_member",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
