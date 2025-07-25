# Generated by Django 5.2.3 on 2025-06-30 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("session_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HealthPredictionResult",
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
                ("health_recommendation", models.TextField()),
                ("criteria_details", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="predictions",
                        to="session_app.session",
                    ),
                ),
            ],
        ),
    ]
