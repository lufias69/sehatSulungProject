# Generated by Django 5.2.3 on 2025-06-20 14:48

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="QuestionCategory",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "image",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionType",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "image",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
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
                ("question_text", models.TextField()),
                ("is_mandatory", models.BooleanField(default=True)),
                (
                    "image",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="question_app.questioncategory",
                    ),
                ),
                (
                    "question_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="question_app.questiontype",
                    ),
                ),
            ],
        ),
    ]
