# Generated by Django 5.2.3 on 2025-06-23 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MediaItem",
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
                ("title", models.CharField(max_length=255)),
                (
                    "media_type",
                    models.CharField(
                        choices=[("image", "Image"), ("video", "Video")], max_length=10
                    ),
                ),
                ("file", models.FileField(upload_to="media/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
