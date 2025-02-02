# Generated by Django 5.0.4 on 2025-01-21 02:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
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
                (
                    "address_type",
                    models.CharField(
                        choices=[("billing", "Billing"), ("shipping", "Shipping")],
                        default="shipping",
                        max_length=120,
                    ),
                ),
                ("street", models.CharField(default="", max_length=255)),
                (
                    "complement",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "neighborhood",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "number",
                    models.CharField(blank=True, default="", max_length=10, null=True),
                ),
                ("city", models.CharField(default="", max_length=100)),
                ("state", models.CharField(default="", max_length=100)),
                ("country", models.CharField(default="", max_length=100)),
                ("postal_code", models.CharField(default="", max_length=20)),
                (
                    "billing_profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billing.billingprofile",
                    ),
                ),
            ],
        ),
    ]
