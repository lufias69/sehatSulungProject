# fitur_app/views.py
import os

from cloudinary.uploader import upload
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from alamat_app.models import Provinsi
from .models import Feature

from dotenv import load_dotenv
import cloudinary


# 🔹 Load variabel dari .env
load_dotenv()

# 🔹 Konfigurasi Cloudinary (Jika belum dilakukan di settings.py)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# views.py
import json

@login_required
def feature_detail(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    questions = feature.questions.prefetch_related('choices').all()

    # Tambahkan list hasil parsing JSON ke setiap question
    # for q in questions:
    #     parsed_choices = []
    #     for c in q.choices.all():
    #         try:
    #             parsed = json.loads(c.choice_text)
    #             print(type(parsed))
    #         except json.JSONDecodeError:
    #             parsed = {"label": c.choice_text}
    #         parsed_choices.append(parsed)
    #
    #     q.choice_json_list = parsed_choices  # ← Tambahkan atribut baru ke question


    return render(request, 'fitur_app/feature_detail.html', {
        'feature': feature,
        'questions': questions,
        'questions_count': questions.count(),
    })

# def feature_detail(request, pk):
#     # Ambil objek fitur berdasarkan primary key
#     feature = get_object_or_404(Feature, pk=pk)
#
#     # Ambil semua pertanyaan yang terkait dengan fitur ini (prefetch choices untuk efisiensi)
#     questions = feature.questions.prefetch_related('choices').all()
#
#     context = {
#         'feature': feature,
#         'questions': questions,
#         'questions_count': questions.count(),
#     }
#
#     return render(request, 'fitur_app/feature_detail.html', context)

# def feature_detail(request, pk):
#     feature = get_object_or_404(Feature, pk=pk)
#     questions = feature.questions.all()  # Ambil semua pertanyaan yang terkait dengan fitur ini
#
#
#     return render(request, 'fitur_app/feature_detail.html', {
#         'feature': feature,
#         'questions': questions,
#         'questions_count': questions.count(),  # Jumlah pertanyaan
#     })


# fitur_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Feature
from .forms import FeatureForm, CheckupGroupForm  # Form untuk menambah dan mengedit fitur

# Menampilkan daftar semua fitur
@login_required
def view_features(request):
    features = Feature.objects.all()  # Mengambil semua fitur
    return render(request, 'fitur_app/view_features.html', {'features': features})

# View untuk menambahkan fitur baru
@login_required
def create_feature(request):
    if request.method == 'POST':
        form = FeatureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Simpan fitur baru
            return redirect('fitur_app:view_features')  # Redirect ke halaman fitur setelah menyimpan
    else:
        form = FeatureForm()

    return render(request, 'fitur_app/create_feature.html', {'form': form})

# View untuk mengedit fitur
@login_required
def edit_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    if request.method == 'POST':
        form = FeatureForm(request.POST, request.FILES, instance=feature)
        if form.is_valid():
            form.save()  # Simpan perubahan fitur
            return redirect('fitur_app:view_features')  # Redirect setelah menyimpan
    else:
        form = FeatureForm(instance=feature)

    return render(request, 'fitur_app/edit_feature.html', {'form': form})

# View untuk menghapus fitur
@login_required
def delete_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    feature.delete()  # Menghapus fitur
    return redirect('fitur_app:view_features')  # Redirect setelah menghapus


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import CheckupCategory
from .forms import CheckupCategoryForm

# Menampilkan daftar kategori
@login_required
def checkup_category_list(request):
    categories = CheckupCategory.objects.all()  # Mengambil semua kategori
    return render(request, 'fitur_app/checkup_category_list.html', {'categories': categories})

# Membuat kategori baru
@login_required
def checkup_category_create(request):
    if request.method == 'POST':
        form = CheckupCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fitur_app:checkup_category_list')  # Kembali ke daftar kategori setelah berhasil menyimpan
    else:
        form = CheckupCategoryForm()
    return render(request, 'fitur_app/checkup_category_form.html', {'form': form})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CheckupGroupForm
from .models import CheckupCategory, CheckupGroup

@login_required
def checkup_group_create(request, kategori_id):
    # Mengambil data Provinsi

    kategori = get_object_or_404(CheckupCategory, id=kategori_id)  # Mendapatkan objek kategori berdasarkan ID

    if request.method == 'POST':
        # Inisialisasi form dengan data POST dan file yang di-upload
        form = CheckupGroupForm(request.POST, request.FILES, kategori=kategori)

        if form.is_valid():
            # Membuat instance CheckupGroup tanpa langsung menyimpan ke database
            checkup_group = form.save(commit=False)
            checkup_group.kategori = kategori  # Menetapkan kategori yang dipilih
            checkup_group.user = request.user  # Mengaitkan pengguna yang sedang login
            checkup_group.save()  # Menyimpan data ke database

            # Setelah data berhasil disimpan, alihkan ke halaman detail checkup
            return redirect('checkup_app:checkup_group_detail', group_id=checkup_group.id)
    else:
        # Jika request GET, buat form kosong
        form = CheckupGroupForm(kategori=kategori)

    # Render form di template
    return render(request, 'checkup_app/checkup_group_form.html', {'form': form, 'kategori': kategori})



# Mengedit kategori yang sudah ada
def checkup_category_update(request, category_id):
    category = get_object_or_404(CheckupCategory, id=category_id)
    print("masuk sini")
    if request.method == 'POST':
        form = CheckupCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('fitur_app:checkup_category_list')  # Kembali ke daftar kategori setelah berhasil memperbarui
    else:
        form = CheckupCategoryForm(instance=category)
    return render(request, 'fitur_app/checkup_category_form.html', {'form': form})

# Menghapus kategori
@login_required
def checkup_category_delete(request, category_id):
    category = get_object_or_404(CheckupCategory, id=category_id)
    category.delete()
    return redirect('fitur_app:checkup_category_list')  # Kembali ke daftar kategori setelah berhasil menghapus
