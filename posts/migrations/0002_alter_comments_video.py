# Generated by Django 5.1 on 2024-09-07 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comments",
            name="video",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="posts.video",
            ),
        ),
    ]
