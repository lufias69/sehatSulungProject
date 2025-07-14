# alamat_app/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import AlamatForm
from .models import KabupatenKota, Kecamatan, Desa

def get_kabupaten_kota(request):
    provinsi_id = request.GET.get('provinsi_id')
    kabupaten_kota = KabupatenKota.objects.filter(provinsi_id=provinsi_id).values('id', 'nama')
    return JsonResponse(list(kabupaten_kota), safe=False)

def get_kecamatan(request):
    kabupaten_kota_id = request.GET.get('kabupaten_kota_id')
    kecamatan = Kecamatan.objects.filter(kabupaten_kota_id=kabupaten_kota_id).values('id', 'nama')
    return JsonResponse(list(kecamatan), safe=False)

def get_desa(request):
    kecamatan_id = request.GET.get('kecamatan_id')
    desa = Desa.objects.filter(kecamatan_id=kecamatan_id).values('id', 'nama')
    return JsonResponse(list(desa), safe=False)

def submit_alamat(request):
    if request.method == 'POST':
        form = AlamatForm(request.POST)
        if form.is_valid():
            # Menyimpan data alamat yang dipilih
            alamat = form.save()
            return redirect('alamat_app:success')  # Mengarahkan setelah berhasil
    else:
        form = AlamatForm()

    return render(request, 'alamat_app/submit_alamat.html', {'form': form})


# alamat_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Provinsi, KabupatenKota, Kecamatan, Desa
from .forms import ProvinsiForm, KabupatenKotaForm, KecamatanForm, DesaForm

def provinsi_list(request):
    provinsi_list = Provinsi.objects.all()
    return render(request, 'alamat_app/provinsi_list.html', {'provinsi_list': provinsi_list})

def add_provinsi(request):
    if request.method == 'POST':
        form = ProvinsiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alamat_app:provinsi_list')
    else:
        form = ProvinsiForm()
    return render(request, 'alamat_app/add_provinsi.html', {'form': form})

# View untuk mengedit Provinsi
def edit_provinsi(request, provinsi_id):
    provinsi = get_object_or_404(Provinsi, id=provinsi_id)
    if request.method == 'POST':
        form = ProvinsiForm(request.POST, instance=provinsi)
        if form.is_valid():
            form.save()
            return redirect('alamat_app:provinsi_list')  # Redirect ke halaman daftar provinsi
    else:
        form = ProvinsiForm(instance=provinsi)
    return render(request, 'alamat_app/edit_provinsi.html', {'form': form, 'provinsi': provinsi})

# View untuk menghapus Provinsi (soft delete)
def delete_provinsi(request, provinsi_id):
    provinsi = get_object_or_404(Provinsi, id=provinsi_id)
    provinsi.delete()
    return redirect('alamat_app:provinsi_list')

def kabupaten_list(request, provinsi_id):
    provinsi = get_object_or_404(Provinsi, id=provinsi_id)
    kabupaten_list = KabupatenKota.objects.filter(provinsi=provinsi)
    return render(request, 'alamat_app/kabupaten_list.html', {'kabupaten_list': kabupaten_list, 'provinsi': provinsi})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Provinsi, KabupatenKota
from .forms import KabupatenForm  # Asumsikan Anda sudah membuat form untuk Kabupaten

def add_kabupaten(request, provinsi_id):
    provinsi = get_object_or_404(Provinsi, id=provinsi_id)

    if request.method == 'POST':
        form = KabupatenForm(request.POST)
        if form.is_valid():
            kabupaten = form.save(commit=False)
            kabupaten.provinsi = provinsi  # Menetapkan provinsi yang dipilih
            kabupaten.save()
            return redirect('alamat_app:provinsi_list')#, provinsi_id=provinsi.id)
    else:
        form = KabupatenForm()

    return render(request, 'alamat_app/add_kabupaten.html', {'form': form, 'provinsi': provinsi})
# View untuk mengedit Kabupaten
def edit_kabupaten(request, kabupaten_id):
    kabupaten = get_object_or_404(KabupatenKota, id=kabupaten_id)
    if request.method == 'POST':
        form = KabupatenKotaForm(request.POST, instance=kabupaten)
        if form.is_valid():
            form.save()
            return redirect('alamat_app:provinsi_list')#, provinsi_id=kabupaten.provinsi.id)
    else:
        form = KabupatenKotaForm(instance=kabupaten)
    return render(request, 'alamat_app/edit_kabupaten.html', {'form': form, 'kabupaten': kabupaten})

# View untuk menghapus Kabupaten (soft delete)
def delete_kabupaten(request, kabupaten_id):
    kabupaten = get_object_or_404(KabupatenKota, id=kabupaten_id)
    kabupaten.delete()
    return redirect('alamat_app:provinsi_list')#, provinsi_id=kabupaten.provinsi.id)

def kecamatan_list(request, kabupaten_id):
    kabupaten = get_object_or_404(KabupatenKota, id=kabupaten_id)
    kecamatan_list = Kecamatan.objects.filter(kabupaten_kota=kabupaten)
    return render(request, 'alamat_app/kecamatan_list.html', {'kecamatan_list': kecamatan_list, 'kabupaten': kabupaten})

from .forms import KecamatanForm  # Asumsikan Anda sudah membuat form untuk Kecamatan

from django.shortcuts import render, get_object_or_404, redirect
from .models import KabupatenKota, Kecamatan
from .forms import KecamatanForm  # Assuming you have a form for Kecamatan

def add_kecamatan(request, kabupaten_id):
    kabupaten = get_object_or_404(KabupatenKota, id=kabupaten_id)

    if request.method == 'POST':
        form = KecamatanForm(request.POST)
        if form.is_valid():
            # Make sure to assign the kabupaten_kota (Kabupaten) field
            kecamatan = form.save(commit=False)
            kecamatan.kabupaten_kota = kabupaten  # Assign the correct Kabupaten
            kecamatan.save()
            return redirect('alamat_app:provinsi_list')#, kabupaten_id=kabupaten.id)  # Redirect to list of kecamatan for this kabupaten
    else:
        form = KecamatanForm()

    return render(request, 'alamat_app/add_kecamatan.html', {'form': form, 'kabupaten': kabupaten})


# View untuk mengedit Kecamatan
def edit_kecamatan(request, kecamatan_id):
    kecamatan = get_object_or_404(Kecamatan, id=kecamatan_id)
    if request.method == 'POST':
        form = KecamatanForm(request.POST, instance=kecamatan)
        if form.is_valid():
            form.save()
            return redirect('alamat_app:provinsi_list')#, kabupaten_id=kecamatan.kabupaten.id)
    else:
        form = KecamatanForm(instance=kecamatan)
    return render(request, 'alamat_app/edit_kecamatan.html', {'form': form, 'kecamatan': kecamatan})

# View untuk menghapus Kecamatan (soft delete)
def delete_kecamatan(request, kecamatan_id):
    kecamatan = get_object_or_404(Kecamatan, id=kecamatan_id)
    kecamatan.delete()
    return redirect('alamat_app:provinsi_list')#, kabupaten_id=kecamatan.kabupaten.id)


def desa_list(request, kecamatan_id):
    kecamatan = get_object_or_404(Kecamatan, id=kecamatan_id)
    desa_list = Desa.objects.filter(kecamatan=kecamatan)
    return render(request, 'alamat_app/desa_list.html', {'desa_list': desa_list, 'kecamatan': kecamatan})

from .forms import DesaForm  # Asumsikan Anda sudah membuat form untuk Desa

def add_desa(request, kecamatan_id):
    kecamatan = get_object_or_404(Kecamatan, id=kecamatan_id)

    if request.method == 'POST':
        form = DesaForm(request.POST)
        if form.is_valid():
            desa = form.save(commit=False)
            desa.kecamatan = kecamatan  # Menetapkan kecamatan yang dipilih
            desa.save()
            # return redirect('alamat_app:provinsi_list', kecamatan_id=kecamatan.id)
            return redirect('alamat_app:provinsi_list')
    else:

        form = DesaForm()

    return render(request, 'alamat_app/add_desa.html', {'form': form, 'kecamatan': kecamatan})# View untuk mengedit Desa

def edit_desa(request, desa_id):
    desa = get_object_or_404(Desa, id=desa_id)
    if request.method == 'POST':
        form = DesaForm(request.POST, instance=desa)
        if form.is_valid():
            form.save()
            # return redirect('alamat_app:provinsi_list', kecamatan_id=desa.kecamatan.id)
            return redirect('alamat_app:provinsi_list')
    else:
        form = DesaForm(instance=desa)
    return render(request, 'alamat_app/edit_desa.html', {'form': form, 'desa': desa})

# View untuk menghapus Desa (soft delete)
def delete_desa(request, desa_id):
    desa = get_object_or_404(Desa, id=desa_id)
    desa.delete()
    # desa.is_deleted = True  # Soft delete
    # desa.save()
    return redirect('alamat_app:provinsi_list')


from django.shortcuts import render
from .models import Desa
from .forms import DesaSearchForm

def desa_search(request):
    form = DesaSearchForm(request.GET or None)
    desa_list = None
    if form.is_valid():
        search = form.cleaned_data['search']
        if search:
            desa_list = Desa.objects.filter(nama__icontains=search).select_related('kecamatan__kabupaten__provinsi')
        else:
            desa_list = Desa.objects.all().select_related('kecamatan__kabupaten__provinsi')

    return render(request, 'alamat_app/desa_search.html', {'form': form, 'desa_list': desa_list})

def select_desa(request, desa_id):
    desa = get_object_or_404(Desa, id=desa_id)
    # Do something with the selected desa
    return render(request, 'alamat_app/selected_desa.html', {'desa': desa})



def filter_kabupaten_by_provinsi(request):
    provinsi_id = request.GET.get('provinsi_id')
    kabupaten_list = KabupatenKota.objects.filter(provinsi_id=provinsi_id).values('id', 'nama')
    return JsonResponse(list(kabupaten_list), safe=False)


def filter_kecamatan_by_kabupaten(request):
    # Mengambil id kabupaten_kota dari query string
    kabupaten_id = request.GET.get('kabupaten_kota_id')  # Nama parameter query string harus sesuai dengan yang diterima
    if kabupaten_id:
        # Filter Kecamatan berdasarkan kabupaten_kota_id
        kecamatan_list = Kecamatan.objects.filter(kabupaten_kota_id=kabupaten_id).values('id', 'nama')
        return JsonResponse(list(kecamatan_list), safe=False)
    return JsonResponse({"error": "Kabupaten ID tidak ditemukan."}, status=400)

def filter_desa_by_kecamatan(request):
    kecamatan_id = request.GET.get('kecamatan_id')
    desa_list = Desa.objects.filter(kecamatan_id=kecamatan_id).values('id', 'nama')
    return JsonResponse(list(desa_list), safe=False)
