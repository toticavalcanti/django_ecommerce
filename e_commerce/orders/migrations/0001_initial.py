# Generated by Django 5.0.4 on 2025-01-17 00:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("addresses", "0001_initial"),
        ("billing", "0001_initial"),
        ("carts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("order_id", models.CharField(blank=True, max_length=120)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Criado"),
                            ("paid", "Pago"),
                            ("shipped", "Enviado"),
                            ("refunded", "Devolvido"),
                        ],
                        default="created",
                        max_length=120,
                    ),
                ),
                (
                    "shipping_total",
                    models.DecimalField(decimal_places=2, default=5.99, max_digits=100),
                ),
                (
                    "total",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "billing_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="billing_address",
                        to="addresses.address",
                    ),
                ),
                (
                    "billing_profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billing.billingprofile",
                    ),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="carts.cart",
                    ),
                ),
                (
                    "shipping_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shipping_address",
                        to="addresses.address",
                    ),
                ),
            ],
        ),
    ]
