# Generated by Django 5.0.4 on 2025-01-20 19:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("title", models.CharField(max_length=120)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("description", models.TextField()),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=100.0, max_digits=20),
                ),
                (
                    "discount_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                ("stock", models.PositiveIntegerField(default=0)),
                (
                    "sku",
                    models.CharField(blank=True, max_length=20, null=True, unique=True),
                ),
                ("featured", models.BooleanField(default=False)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="categories.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                ("image", models.ImageField(upload_to="products/")),
                ("alt_text", models.CharField(blank=True, max_length=255, null=True)),
                ("is_featured", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=0)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
