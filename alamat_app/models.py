# alamat_app/models.py
from django.db import models

from hash_app.utils import generate_unique_hash


class Provinsi(models.Model):
    nama = models.CharField(max_length=100)
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama


class KabupatenKota(models.Model):
    provinsi = models.ForeignKey(Provinsi, related_name='kabupaten_kota', on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama


class Kecamatan(models.Model):
    kabupaten_kota = models.ForeignKey(KabupatenKota, related_name='kecamatan', on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama


class Desa(models.Model):
    kecamatan = models.ForeignKey(Kecamatan, related_name='desa', on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama
