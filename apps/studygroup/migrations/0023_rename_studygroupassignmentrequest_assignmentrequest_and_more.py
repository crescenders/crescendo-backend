# Generated by Django 4.2.6 on 2023-10-28 18:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("studygroup", "0022_alter_studygroupassignmentsubmission_options_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="StudyGroupAssignmentRequest",
            new_name="AssignmentRequest",
        ),
        migrations.RenameModel(
            old_name="StudyGroupAssignmentSubmission",
            new_name="AssignmentSubmission",
        ),
    ]
