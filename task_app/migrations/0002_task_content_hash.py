# Generated by Django 5.2.3 on 2025-07-14 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="content_hash",
            field=models.CharField(
                blank=True, editable=False, max_length=64, null=True
            ),
        ),
    ]
