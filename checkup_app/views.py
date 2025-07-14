# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from alamat_app.models import Provinsi
from analisis_ai.models import HealthPredictionResult
from fitur_app.forms import CheckupCategoryForm
from session_app.models import Session
from .forms import CheckupGroupForm
from fitur_app.models import CheckupGroup


@login_required
def checkup_group_create(request, kategori_id):
    kategori = get_object_or_404(CheckupCategory, id=kategori_id)
    provinsi_list = Provinsi.objects.all()
    print(provinsi_list)

    if request.method == 'POST':
        form = CheckupGroupForm(request.POST, request.FILES, kategori=kategori)
        if form.is_valid():
            # Menyimpan data ke database setelah validasi berhasil
            checkup_group = form.save(commit=False)
            checkup_group.kategori = kategori  # Menetapkan kategori yang dipilih
            checkup_group.user = request.user  # Menetapkan pengguna yang sedang login
            print(checkup_group)
            checkup_group.save()
            return redirect('checkup_app:checkup_group_detail', group_id=checkup_group.id)  # Redirect ke halaman detail

        else:
            print("Form invalid")
            print(form.errors)  # Print error untuk mengetahui apa yang salah

    else:
        form = CheckupGroupForm(kategori=kategori)

    return render(request, 'checkup_app/checkup_group_form.html', {'form': form, 'kategori': kategori, 'provinsi_list': provinsi_list})

@login_required
def checkup_group_edit(request, group_id):
    provinsi_list = Provinsi.objects.all()
    print(provinsi_list)

    checkup_group = get_object_or_404(CheckupGroup, id=group_id, user=request.user, is_deleted=False)
    kategori = checkup_group.kategori

    if request.method == 'POST':
        form = CheckupGroupForm(request.POST, request.FILES, instance=checkup_group, kategori=kategori)
        if form.is_valid():
            form.save()
            return redirect('checkup_app:checkup_group_list')#, group_id=checkup_group.id)
        else:
            print("Form invalid")
            print(form.errors)
    else:
        form = CheckupGroupForm(instance=checkup_group, kategori=kategori)

    return render(request, 'checkup_app/checkup_group_form.html', {'form': form, 'kategori': kategori, 'provinsi_list': provinsi_list})


def checkup_category_update(request, category_id):
    # Ambil kategori yang ingin diperbarui berdasarkan ID
    category = get_object_or_404(CheckupCategory, id=category_id)

    print(category)

    if request.method == 'POST':
        # Jika metode POST, perbarui kategori dengan data yang dikirimkan
        form = CheckupCategoryForm(request.POST, instance=category)
        if form.is_valid():
            print("Form valid")
            form.save()
        else:
            print("Form invalid")
            return redirect('checkup_app:checkup_category_list')  # Redirect ke halaman daftar kategori setelah berhasil update
    else:
        print("Metode GET")
        # Jika metode GET, tampilkan form dengan data kategori yang ada
        form = CheckupCategoryForm(instance=category)

    return render(request, 'checkup_app/checkup_category_form.html', {'form': form, 'category': category})
@login_required
def checkup_group_delete(request, group_id):
    checkup_group = get_object_or_404(CheckupGroup, id=group_id, user=request.user, is_deleted=False)

    if request.method == 'POST':
        checkup_group.is_deleted = True
        checkup_group.save()
        return redirect('checkup_app:checkup_group_list')

    return render(request, 'checkup_app/checkup_group_confirm_delete.html', {'checkup_group': checkup_group})

# def checkup_group_create(request, kategori_id):
#     kategori = get_object_or_404(CheckupCategory, id=kategori_id)
#
#     if request.method == 'POST':
#         form = CheckupGroupForm(request.POST, request.FILES, kategori=kategori)  # Passing category to form
#         if form.is_valid():
#             checkup_group = form.save(commit=False)
#             checkup_group.kategori = kategori  # Set the selected category
#             checkup_group.user = request.user  # Assign the current logged-in user
#             checkup_group.save()
#             return redirect('checkup_app:checkup_group_detail', group_id=checkup_group.id)  # After saving, show detail page
#     else:
#         form = CheckupGroupForm(kategori=kategori)
#
#     return render(request, 'checkup_app/checkup_group_form.html', {'form': form, 'kategori': kategori})


def checkup_group_detail(request, group_id):
    group = CheckupGroup.objects.get(id=group_id)
    fitur = group.get_relevant_features()

    # Ambil fitur yang relevan berdasarkan kategori dan umur
    # print(fitur)
    # try:
    #     latest_session = Session.objects.filter(checkup_group=group_id, feature=fitur).order_by(
    #         '-created_at').first()
    #
    #     criteria_details = []
    #     health_recommendation = ""
    #     if HealthPredictionResult.objects.filter(session=latest_session):
    #         x = HealthPredictionResult.objects.filter(session=latest_session)
    #         for i in x:
    #             for j in i.criteria_details:
    #                 print(j)
    #                 criteria_details.append(j)
    #             health_recommendation = i.health_recommendation
    #             # print(i.criteria_details)
    #     else:
    #         x = []
    #         print("no")
    # except HealthPredictionResult.DoesNotExist:
    #     criteria_details = []
    #     health_recommendation = ""

    return render(request, 'checkup_app/checkup_group_detail.html', {'group': group,
                                                                     'fitur': fitur,
                                                                     # 'latest_session':latest_session,
                                                                     # 'criteria_details': criteria_details,
                                                                     # 'health_recommendation': health_recommendation,
                                                                     # 'HealthPredictionResult': x
                                                                     })

# views.py
from django.shortcuts import render, redirect
from .forms import CategorySelectionForm
from fitur_app.models import CheckupCategory

def select_category(request):
    if request.method == 'POST':
        form = CategorySelectionForm(request.POST)
        if form.is_valid():
            kategori = form.cleaned_data['kategori']
            return redirect('checkup_app:checkup_group_create', kategori_id=kategori.id)
    else:
        form = CategorySelectionForm()

    return render(request, 'checkup_app/select_category.html', {'form': form})

# views.py
from django.shortcuts import render
from fitur_app.models import CheckupGroup

# def checkup_group_list(request):
#     # Ambil semua CheckupGroup dan urutkan berdasarkan tanggal pendaftaran (tanggal_pendaftaran)
#     checkup_groups = CheckupGroup.objects.all().order_by('-tanggal_pendaftaran')
#
#     return render(request, 'checkup_app/checkup_group_list.html', {'checkup_groups': checkup_groups})


@login_required
def checkup_group_list(request):
    # Ambil semua CheckupGroup yang dibuat oleh user yang sedang login
    # checkup_groups = CheckupGroup.objects.filter(user=request.user).order_by('-tanggal_pendaftaran')
    checkup_groups = CheckupGroup.objects.filter(user=request.user, is_deleted=False).order_by('-tanggal_pendaftaran')
    checkup_groups_list = []
    # HealthPredictionResult.objects.filter(user=request.user).order_by('-created_at')
    counter = 0
    for i in checkup_groups:
        print(counter)
        counter = counter + 1
        x = HealthPredictionResult.objects.filter(session__checkup_group=i).order_by('-created_at')
        print(i.desa)

        # print(x)
        analisis_ai_list = []
        kriteria_list = []
        created_at_list = []
        for j in x:
            created_at_list.append(j.created_at.strftime("%d/%m/%Y %H:%M:%S"))
            kriteria_list.append(j.criteria_details)
            analisis_ai_list.append(j.health_recommendation)
            # print(j)
        checkup_groups_list.append({'checkup_groups': i,'analisis_ai_list':analisis_ai_list, 'kriteria_list':kriteria_list , 'created_at_list':created_at_list })
        print(created_at_list)
    return render(request, 'checkup_app/checkup_group_list.html', {'checkup_groups': checkup_groups_list})

