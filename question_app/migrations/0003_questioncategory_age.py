# Generated by Django 5.2.3 on 2025-06-20 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("question_app", "0002_question_feature_choice_useranswer"),
    ]

    operations = [
        migrations.AddField(
            model_name="questioncategory",
            name="age",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
