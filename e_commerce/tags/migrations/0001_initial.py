# Generated by Django 5.0.4 on 2025-01-21 02:34

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("slug", models.SlugField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("active", models.BooleanField(default=True)),
                ("products", models.ManyToManyField(blank=True, to="products.product")),
            ],
        ),
    ]
