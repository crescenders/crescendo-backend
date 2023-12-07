# Generated by Django 4.2.6 on 2023-12-07 05:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_alter_user_username"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "User", "verbose_name_plural": "Users"},
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=80, unique=True, verbose_name="email"),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_admin",
            field=models.BooleanField(default=False, verbose_name="is_admin"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=64, verbose_name="username"),
        ),
    ]
