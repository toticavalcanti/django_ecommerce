# Generated by Django 5.0.4 on 2025-01-21 02:34

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("full_name", models.CharField(blank=True, max_length=255, null=True)),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("active", models.BooleanField(default=True)),
                ("staff", models.BooleanField(default=False)),
                ("admin", models.BooleanField(default=False)),
                (
                    "is_verified",
                    models.BooleanField(
                        default=False,
                        help_text="Indica se o email do usuário foi verificado.",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="GuestEmail",
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
                ("email", models.EmailField(max_length=254)),
                ("active", models.BooleanField(default=True)),
                ("update", models.DateTimeField(auto_now=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
