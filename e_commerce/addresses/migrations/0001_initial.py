# Generated by Django 5.0.4 on 2025-01-13 23:18

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
                        max_length=120,
                    ),
                ),
                ("address_line_1", models.CharField(max_length=120)),
                (
                    "address_line_2",
                    models.CharField(blank=True, max_length=120, null=True),
                ),
                ("city", models.CharField(max_length=120)),
                ("country", models.CharField(default="Brazil", max_length=120)),
                ("state", models.CharField(max_length=120)),
                ("postal_code", models.CharField(max_length=120)),
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
