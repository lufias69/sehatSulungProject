import hashlib
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models


def compute_model_hash(instance, fields):
    """
    Fungsi untuk menghitung hash untuk instance berdasarkan fields yang diberikan.
    Menangani ForeignKey dengan hanya menyertakan ID.
    """
    data = {}

    for field in fields:
        value = getattr(instance, field)

        # Jika value adalah objek model (misalnya ForeignKey), gunakan ID-nya
        if isinstance(value, models.Model):
            value = value.id  # Ambil ID dari objek model (ForeignKey)

        data[field] = value

    # Mengonversi data menjadi JSON terurut
    json_data = json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True)

    # Menghasilkan hash SHA256 untuk seluruh data
    return hashlib.sha256(json_data.encode('utf-8')).hexdigest()
# def compute_model_hash(instance, fields):
#     """
#     Fungsi untuk menghitung hash untuk model instance berdasarkan fields yang diberikan.
#     """
#     data = {field: getattr(instance, field) for field in fields}
#     json_data = json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True)
#     return hashlib.sha256(json_data.encode('utf-8')).hexdigest()

def compute_table_hash(model_class):
    """
    Fungsi untuk menghitung hash dari seluruh tabel.
    """
    # Ambil semua data dari model yang diberikan
    objects = model_class.objects.all()

    # Membuat data JSON dari setiap entri di tabel
    all_data = []
    for obj in objects:
        # Ambil field yang relevan untuk hash
        data = {field.name: getattr(obj, field.name) for field in obj._meta.get_fields() if field.name != 'image'}
        all_data.append(data)

    # Mengonversi data menjadi JSON terurut
    json_data = json.dumps(all_data, cls=DjangoJSONEncoder, sort_keys=True)

#     # Menghasilkan hash SHA256 untuk keseluruhan tabel
#     return hashlib.sha256(json_data.encode('utf-8')).hexdigest()

import time
import hashlib

def generate_unique_hash():
    """
    Generate a unique hash based on the current time in seconds.
    This ensures that the hash is unique and does not repeat.
    """
    current_time = str(time.time())  # Current timestamp in seconds
    return hashlib.sha256(current_time.encode('utf-8')).hexdigest()  # Generate SHA256 hash

