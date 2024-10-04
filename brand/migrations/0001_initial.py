# Generated by Django 5.1.1 on 2024-09-30 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
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
                ("name", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "brand",
                "verbose_name_plural": "brands",
                "ordering": ["name"],
            },
        ),
    ]
