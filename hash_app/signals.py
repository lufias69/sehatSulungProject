import hashlib
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver

from alamat_app.models import Provinsi, KabupatenKota, Kecamatan, Desa
from fitur_app.models import CheckupGroup, Feature, CheckupCategory
from .models import TableHash, ModifiedTableHash
from question_app.models import QuestionType, QuestionCategory, Question, Choice

# def compute_table_hash(model_class):
#     # Ambil semua data dari model yang diberikan
#     objects = model_class.objects.all()
#
#     # Membuat data JSON dari setiap entri di tabel
#     all_data = []
#     for obj in objects:
#         # Ambil field yang relevan untuk hash (hindari field image atau relasi lain yang tidak relevan)
#         data = {field.name: getattr(obj, field.name) for field in obj._meta.get_fields() if field.name != 'image'}
#         all_data.append(data)
#
#     # Mengonversi data menjadi JSON terurut
#     json_data = json.dumps(all_data, cls=DjangoJSONEncoder, sort_keys=True)
#
#     # Menghasilkan hash SHA256 untuk keseluruhan tabel
#     return hashlib.sha256(json_data.encode('utf-8')).hexdigest()
#
# @receiver(post_save, sender=QuestionType)
# @receiver(post_save, sender=QuestionCategory)
# @receiver(post_save, sender=Question)
# @receiver(post_save, sender=Choice)
# def update_table_hash(sender, instance, created, **kwargs):
#     """
#     Fungsi ini akan dijalankan setiap kali data disimpan (insert/update) pada model
#     yang dimonitor dan akan menghitung ulang hash tabel serta memperbarui TableHash.
#     """
#     model_name = sender.__name__
#
#     # Hitung ulang hash untuk tabel model terkait
#     new_hash = compute_table_hash(sender)
#
#     # Cek apakah sudah ada record TableHash untuk model ini
#     table_hash, created = TableHash.objects.get_or_create(model_name=model_name)
#
#     # Perbarui hash dan waktu update
#     table_hash.table_hash = new_hash
#     table_hash.save()
#
#     print(f"Table hash for {model_name} updated: {new_hash}")

from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import Question, TableHash
from .utils import generate_unique_hash


@receiver(post_save, sender=Question)
@receiver(post_save, sender=QuestionType)
@receiver(post_save, sender=QuestionCategory)
@receiver(post_save, sender=Choice)
@receiver(post_save, sender=CheckupGroup)
@receiver(post_save, sender=Feature)
@receiver(post_save, sender=CheckupCategory)
@receiver(post_save, sender=Provinsi)
@receiver(post_save, sender=KabupatenKota)
@receiver(post_save, sender=Kecamatan)
@receiver(post_save, sender=Desa)
def update_table_hash_on_question_save(sender, instance, created, **kwargs):
    """
    Fungsi ini akan dijalankan setiap kali data disimpan (insert/update) pada model
    yang dimonitor (Question) dan akan menghitung ulang hash tabel serta memperbarui TableHash.
    """
    model_name = sender.__name__  # Mendapatkan nama model (misalnya 'Question')

    # Generate a new unique hash for the table
    new_hash = generate_unique_hash()  # Hash baru berdasarkan timestamp

    # Cek apakah sudah ada record TableHash untuk model ini
    table_hash, created = TableHash.objects.get_or_create(model_name=model_name)

    # Perbarui hash dan waktu update
    table_hash.table_hash = new_hash
    table_hash.save()

    print(f"Table hash for {model_name} updated: {new_hash}")

@receiver(post_save, sender=TableHash)
def update_modified_table_hash(sender, instance, created, **kwargs):
    """
    Fungsi ini akan dijalankan setiap kali data disimpan (insert/update) pada model
    yang dimonitor (Question) dan akan menghitung ulang hash tabel serta memperbarui TableHash.
    """
    model_name = sender.__name__  # Mendapatkan nama model (misalnya 'Question')

    # Generate a new unique hash for the table
    new_hash = generate_unique_hash()  # Hash baru berdasarkan timestamp

    # Cek apakah sudah ada record TableHash untuk model ini
    table_hash, created = ModifiedTableHash.objects.get_or_create(model_name=model_name)

    # Perbarui hash dan waktu update
    table_hash.table_hash = new_hash
    table_hash.save()

    print(f"Table hash for {model_name} updated: {new_hash}")

