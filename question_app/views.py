# question_app/views.py
from cloudinary.cache.responsive_breakpoints_cache import instance
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes

from media_center_app.models import MediaItem
from .forms import QuestionForm
from .models import Question

# question_app/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import QuestionForm
from .models import Question, Choice, Feature


# def create_question(request):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             # Simpan soal (pertanyaan)
#             question = form.save(commit=False)
#
#             # Simpan fitur yang dipilih (jika ada)
#             feature_id = request.POST.get('feature')  # Mendapatkan ID fitur yang dipilih
#             if feature_id:
#                 feature = Feature.objects.get(id=feature_id)
#                 question.feature = feature  # Menghubungkan fitur ke soal
#             question.save()  # Simpan pertanyaan pertama
#
#             # Jika jenis pertanyaan adalah Pilihan Ganda atau Centang
#             choices = request.POST.getlist('choices')  # Mendapatkan pilihan yang dimasukkan admin
#             for choice_text in choices:
#                 if choice_text.strip():  # Mengabaikan input kosong
#                     Choice.objects.create(question=question,
#                                           choice_text=choice_text.strip())  # Simpan pilihan ke database
#
#             # Redirect ke halaman daftar pertanyaan setelah berhasil menyimpan
#             return redirect('question_app:view_question_type_category')
#     else:
#         form = QuestionForm()
#
#     return render(request, 'question_app/create_question.html', {'form': form})


# question_app/views.py

from django.shortcuts import render, redirect
from .forms import QuestionTypeForm
@login_required
def create_question_type(request):
    if request.method == 'POST':
        form = QuestionTypeForm(request.POST)
        if form.is_valid():
            form.save()  # Simpan jenis pertanyaan baru
            return redirect('question_app:create_question_type')  # Redirect ke halaman setelah menyimpan
    else:
        form = QuestionTypeForm()

    return render(request, 'question_app/create_question_type.html', {'form': form})


# question_app/views.py

from .forms import QuestionCategoryForm

# question_app/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import QuestionForm
from .models import Feature, Question

# question_app/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import QuestionForm
from .models import Feature, Question

# def create_question(request):
#     feature_id = request.GET.get('feature')  # Mengambil ID fitur dari URL
#     feature = Feature.objects.get(id=feature_id)  # Ambil fitur berdasarkan ID
#
#     if request.method == 'POST':
#         form = QuestionForm(request.POST, request.FILES)  # Menangani data POST dari formulir
#         if form.is_valid():
#             question = form.save(commit=False)  # Jangan langsung simpan, atur fitur terlebih dahulu
#             question.feature = feature  # Menghubungkan fitur yang dipilih ke pertanyaan
#             question.save()  # Simpan pertanyaan ke database
#
#             return redirect('fitur_app:feature_detail', pk=feature.id)  # Redirect ke halaman detail fitur
#         else:
#             # Jika formulir tidak valid, tampilkan pesan error atau kembalikan formulir dengan error
#             return HttpResponse("Form is not valid!")
#     else:
#         form = QuestionForm()
#
#     return render(request, 'question_app/create_question.html', {'form': form, 'feature': feature})

# question_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from .forms import QuestionForm

# Fungsi untuk mengedit pertanyaan
@login_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)  # Ambil pertanyaan berdasarkan pk
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=question)  # Isi form dengan data yang ada
        if form.is_valid():
            form.save()  # Simpan perubahan
            return redirect('fitur_app:feature_detail', pk=question.feature.pk)  # Kembali ke detail fitur
    else:
        form = QuestionForm(instance=question)  # Form untuk mengedit, menggunakan instance

    return render(request, 'question_app/edit_question.html', {'form': form, 'question': question})

# Fungsi untuk menghapus pertanyaan
@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)  # Ambil pertanyaan berdasarkan pk
    feature_pk = question.feature.pk  # Menyimpan ID fitur untuk redirect setelah penghapusan
    question.delete()  # Hapus pertanyaan
    return redirect('fitur_app:feature_detail', pk=feature_pk)  # Redirect ke halaman detail fitur


# def create_question_category(request):
#     if request.method == 'POST':
#         form = QuestionCategoryForm(request.POST)
#         if form.is_valid():
#             form.save()  # Simpan kategori pertanyaan baru
#             return redirect('question_app:create_question_category')  # Redirect ke halaman setelah menyimpan
#     else:
#         form = QuestionCategoryForm()
#
#     return render(request, 'question_app/create_question_category.html', {'form': form})


# question_app/views.py

from django.shortcuts import render, get_object_or_404
from .models import Question

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'question_app/question_detail.html', {'question': question})


# question_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import QuestionType, QuestionCategory
from .forms import QuestionTypeForm, QuestionCategoryForm

# View untuk menampilkan QuestionType dan QuestionCategory
@login_required
def view_question_type_category(request):
    question_types = QuestionType.objects.all()
    question_categories = QuestionCategory.objects.all()

    return render(request, 'question_app/view_question_type_category.html', {
        'question_types': question_types,
        'question_categories': question_categories
    })

# View untuk menambahkan QuestionType
@login_required
def create_question_type(request):
    if request.method == 'POST':
        form = QuestionTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_app:view_question_type_category')
    else:
        form = QuestionTypeForm()
    return render(request, 'question_app/create_question_type.html', {'form': form})

# View untuk menambahkan QuestionCategory
@login_required
def create_question_category(request):
    if request.method == 'POST':
        form = QuestionCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_app:view_question_type_category')
    else:
        form = QuestionCategoryForm()
    return render(request, 'question_app/create_question_category.html', {'form': form})

# View untuk mengedit QuestionType
@login_required
def edit_question_type(request, pk):
    question_type = get_object_or_404(QuestionType, pk=pk)
    if request.method == 'POST':
        form = QuestionTypeForm(request.POST, instance=question_type)
        if form.is_valid():
            form.save()
            return redirect('question_app:view_question_type_category')
    else:
        form = QuestionTypeForm(instance=question_type)
    return render(request, 'question_app/edit_question_type.html', {'form': form})

# View untuk mengedit QuestionCategory
def edit_question_category(request, pk):
    question_category = get_object_or_404(QuestionCategory, pk=pk)
    if request.method == 'POST':
        form = QuestionCategoryForm(request.POST, instance=question_category)
        if form.is_valid():
            form.save()
            return redirect('question_app:view_question_type_category')
    else:
        form = QuestionCategoryForm(instance=question_category)
    return render(request, 'question_app/edit_question_category.html', {'form': form})

# View untuk menghapus QuestionType
def delete_question_type(request, pk):
    question_type = get_object_or_404(QuestionType, pk=pk)
    question_type.delete()
    return redirect('question_app:view_question_type_category')

# View untuk menghapus QuestionCategory
def delete_question_category(request, pk):
    question_category = get_object_or_404(QuestionCategory, pk=pk)
    question_category.delete()
    return redirect('question_app:view_question_type_category')



# question_app/views.py

from rest_framework import viewsets
from .models import Question, Feature, QuestionType
from .serializers import QuestionSerializer, FeatureSerializer, QuestionTypeSerializer

# # ViewSet untuk Question
# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

# ViewSet untuk Feature
class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

# ViewSet untuk QuestionType
class QuestionTypeViewSet(viewsets.ModelViewSet):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer

# question_app/views.py

from rest_framework import viewsets
from .models import QuestionCategory
from .serializers import QuestionCategorySerializer

class QuestionCategoryViewSet(viewsets.ModelViewSet):
    queryset = QuestionCategory.objects.all()
    serializer_class = QuestionCategorySerializer

# question_app/views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from .models import Question, Feature
from .serializers import QuestionSerializer
from rest_framework import status



class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]  # All methods require admin permissions

    def create(self, request, *args, **kwargs):
        """
        Menyimpan pertanyaan baru dan mengaitkannya dengan fitur.
        """
        feature_id = request.data.get('feature')
        if not feature_id:
            return Response({'detail': 'Feature ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            feature = Feature.objects.get(pk=feature_id)
        except Feature.DoesNotExist:
            return Response({'detail': 'Feature not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(feature=feature)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Action untuk menambahkan pertanyaan baru
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def add_question(self, request, pk=None):
        try:
            feature = Feature.objects.get(pk=pk)  # Ambil fitur berdasarkan ID
        except Feature.DoesNotExist:
            return Response({"detail": "Feature not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(feature=feature)  # Simpan pertanyaan dengan fitur yang dipilih
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Action untuk update pertanyaan
    @action(detail=True, methods=['put'], permission_classes=[IsAdminUser])
    def update_question(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({"detail": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Action untuk menghapus pertanyaan
    @action(detail=True, methods=['delete'], permission_classes=[IsAdminUser])
    def delete_question(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({"detail": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     permission_classes = [IsAdminUser]
#
#     def create(self, request, *args, **kwargs):
#         """
#         Menyimpan pertanyaan baru dan mengaitkannya dengan fitur.
#         """
#         feature_id = request.data.get('feature')
#         if not feature_id:
#             return Response({'detail': 'Feature ID is required'}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             feature = Feature.objects.get(pk=feature_id)
#         except Feature.DoesNotExist:
#             return Response({'detail': 'Feature not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(feature=feature)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # Action untuk menambahkan pertanyaan baru
#     @action(detail=True, methods=['post'])
#     def add_question(self, request, pk=None):
#         # print(pk)
#         try:
#             feature = Feature.objects.get(pk=pk)  # Ambil fitur berdasarkan ID
#         except Feature.DoesNotExist:
#             return Response({"detail": "Feature not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(feature=feature)  # Simpan pertanyaan dengan fitur yang dipilih
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # Action untuk update pertanyaan
#     @action(detail=True, methods=['put'])
#     def update_question(self, request, pk=None):
#         question = Question.objects.get(pk=pk)  # Ambil pertanyaan berdasarkan ID
#         # serializer = QuestionSerializer(question, data=request.data)
#         serializer = QuestionSerializer(instance, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # Action untuk menghapus pertanyaan
#     @action(detail=True, methods=['delete'])
#     def delete_question(self, request, pk=None):
#         question = Question.objects.get(pk=pk)
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# def add_update_delete_question(request, pk, question_id):
#     # Ambil fitur berdasarkan pk (feature ID)
#     feature = get_object_or_404(Feature, id=pk)
#     question = get_object_or_404(Question, id=question_id, feature=feature)
#
#     if question_id:
#         question = get_object_or_404(Question, id=question_id, feature=feature)
#     else:
#         question = None
#
#     if request.method == 'POST':
#         form = QuestionForm(request.POST, request.FILES, instance=question)
#         if form.is_valid():
#             new_question = form.save(commit=False)
#             new_question.feature = feature
#             new_question.save()
#             return redirect('fitur_app:feature_detail', pk=feature.id)
#         else:
#             return HttpResponse("Form tidak valid.")
#     else:
#         form = QuestionForm(instance=question)
#
#     return render(request, 'question_app/add_update_delete_question.html', {
#         'feature': feature,
#         'form': form,
#         'editing': question is not None
#     })

def create_question(request):
    print('buat soal')
    media_items = MediaItem.objects.filter(media_type='image')
    feature_id = request.GET.get('feature_id')
    if not feature_id:
        return HttpResponse("Feature ID is required.", status=400)

    feature = get_object_or_404(Feature, id=feature_id)

    if request.method == 'POST':
        print("POST")
        form = QuestionForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            print(form.cleaned_data)
            question = form.save(commit=False)
            question.feature = feature

            # print(question.objects.all())

            question.save()
            return redirect('fitur_app:feature_detail', pk=feature.id)
    else:
        print("GET")
        form = QuestionForm()
    # print(form)
    return render(request, 'question_app/add_update_delete_question.html', {
        'form': form,
        'feature': feature,
        'question': None,
        'media_items': media_items,
    })

from django.shortcuts import get_object_or_404, render, redirect
from .models import Feature, Question, Choice


from django.http import JsonResponse
import json


def edit_question(request, feature_id, question_id):
    feature = get_object_or_404(Feature, id=feature_id)
    question = get_object_or_404(Question, id=question_id, feature=feature)

    # media_items = MediaItem.objects.filter(media_type='image')

    choices_qs = question.choices.values_list('choice_text', flat=True)

    try:
        # Jika choices disimpan sebagai string JSON
        choices = json.loads(choices_qs[0]) if len(choices_qs) == 1 and isinstance(choices_qs[0], str) else list(choices_qs)
    except Exception:
        choices = list(choices_qs)
    print(choices)
    question_data = {
        'id': question.id,
        'question_text': question.question_text,
        'question_type': question.question_type.id if question.question_type else None,
        'category': question.category.id if question.category else None,
        'choices': choices,
    }

    return render(request, 'question_app/add_update_delete_question.html', {
        'feature': feature,
        'question_id': question.id,
        'question_data': question_data,#json.dumps(question_data),  # kirim ke JS sebagai JSON
        # 'media_items': media_items,
    })

# def edit_question(request, feature_id, question_id):
#     feature = get_object_or_404(Feature, id=feature_id)
#     question = get_object_or_404(Question, id=question_id, feature=feature)
#
#     if request.method == 'POST':
#         form = QuestionForm(request.POST, request.FILES, instance=question)
#         if form.is_valid():
#             form.save()
#             return redirect('fitur_app:feature_detail', pk=feature.id)
#     else:
#         form = QuestionForm(instance=question)
#
#     if question.choices.values():
#         print("isi", )
#     # Ambil data yang akan digunakan di JavaScript
#     question_data = {
#         'id': question.id,
#         'question_text': question.question_text,
#         'question_type': question.question_type.id if question.question_type else None,
#         'category': question.category.id if question.category else None,
#         'choices': list(question.choices.values_list('choice_text', flat=True)),
#     }
#
#     # print(question_data)
#
#     return render(request, 'question_app/add_update_delete_question.html', {
#         'form': form,
#         'feature': feature,
#         'question_id': question.id,
#         'question_data': question_data,
#     })

# def edit_question(request, feature_id, question_id):
#     feature = get_object_or_404(Feature, id=feature_id)
#     question = get_object_or_404(Question, id=question_id, feature=feature)
#
#     if request.method == 'POST':
#         form = QuestionForm(request.POST, request.FILES, instance=question)
#         if form.is_valid():
#             form.save()
#             return redirect('fitur_app:feature_detail', pk=feature.id)
#     else:
#         form = QuestionForm(instance=question)
#
#     return render(request, 'question_app/add_update_delete_question.html', {
#         'form': form,
#         'feature': feature,
#         'question': question,
#     })

from django.shortcuts import get_object_or_404, redirect
from .models import Question, Feature


def delete_question(request, feature_id, question_id):
    feature = get_object_or_404(Feature, id=feature_id)
    question = get_object_or_404(Question, id=question_id, feature=feature)

    if request.method == 'POST':
        question.delete()
        return redirect('fitur_app:feature_detail', pk=feature.id)

    return render(request, 'question_app/confirm_delete.html', {'feature': feature, 'question': question})

