# Generated by Django 5.1 on 2024-09-07 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Profile",
        ),
    ]