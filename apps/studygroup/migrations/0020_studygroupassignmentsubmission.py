# Generated by Django 4.2.6 on 2023-10-25 04:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("studygroup", "0019_rename_assignmentrequest_studygroupassignmentrequest"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudyGroupAssignmentSubmission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=64)),
                ("content", models.TextField(max_length=1500)),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="studygroup.studygroupassignmentrequest",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="studygroup.studygroupmember",
                    ),
                ),
                (
                    "studygroup",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="studygroup.studygroup",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
