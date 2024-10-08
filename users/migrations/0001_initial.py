# Generated by Django 5.1 on 2024-09-03 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("name", models.CharField(max_length=20)),
                ("surname", models.CharField(max_length=20)),
                ("profile_pics", models.ImageField(upload_to="")),
                ("phone", models.CharField(max_length=15)),
            ],
        ),
    ]
