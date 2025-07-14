from django.db import models

from hash_app.utils import generate_unique_hash


class TableHash(models.Model):
    model_name = models.CharField(max_length=255)  # Nama model yang dimonitor
    table_hash = models.CharField(max_length=64)  # Hash dari seluruh tabel
    last_updated = models.DateTimeField(auto_now=True)  # Tanggal terakhir update

    # content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     # Generate a new unique hash (using timestamp)
    #     self.content_hash = generate_unique_hash()  # Use the unique hash generator
    #
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.model_name} - {self.table_hash}"

class ModifiedTableHash(models.Model):
    model_name = models.CharField(max_length=255)  # Nama model yang dimonitor
    table_hash = models.CharField(max_length=64)  # Hash dari seluruh tabel
    last_updated = models.DateTimeField(auto_now=True)  # Tanggal terakhir update

    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.model_name} - {self.table_hash}"
