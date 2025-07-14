# task_app/models.py

from django.db import models
from fitur_app.models import CheckupGroup
from fitur_app.models import Feature
from django.contrib.auth.models import User

from hash_app.utils import generate_unique_hash


class Task(models.Model):
    name = models.CharField(max_length=255)  # Nama task
    task_duration = models.IntegerField()  # Durasi waktu tugas dalam hari (misalnya 1 hari, 7 hari, 30 hari)
    features = models.ManyToManyField(Feature, related_name='tasks')  # Relasi Many-to-Many dengan Feature  # Relasi dengan Feature
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu pembuatan task

    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# class TaskCompletion(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # User yang mengerjakan task
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Task yang dikerjakan
#     checkup_group = models.ForeignKey(CheckupGroup, on_delete=models.CASCADE)  # Checkup group terkait
#     completed_at = models.DateTimeField(auto_now_add=True)  # Waktu kapan task selesai
#
#     def __str__(self):
#         return f"Task {self.task.name} completed by {self.user.username}"
