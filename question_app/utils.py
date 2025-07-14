import hashlib
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

# def compute_model_hash(instance, fields):
#     data = {field: getattr(instance, field) for field in fields}
#     json_data = json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True)
#     return hashlib.sha256(json_data.encode('utf-8')).hexdigest()

# def compute_model_hash(instance, fields):
#     # Ambil nilai dari field yang relevan, pastikan untuk mengambil ID dari relasi (contoh: category_id)
#     data = {}
#     for field in fields:
#         value = getattr(instance, field)
#         if isinstance(value, models.Model):
#             # Jika field adalah objek model, gunakan ID
#             value = value.id
#         data[field] = value
#
#     json_data = json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True)
#     return hashlib.sha256(json_data.encode('utf-8')).hexdigest()
