# Generated by Django 4.2.4 on 2023-08-23 15:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("studygroup", "0003_remove_studygroupmember_studygroup_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="studygroup",
            old_name="user_limit",
            new_name="member_limit",
        ),
    ]
