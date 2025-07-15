# nama_aplikasi_anda/views.py
# from allauth.idp.oidc.contrib.rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions

from alamat_app.models import Provinsi, KabupatenKota, Kecamatan, Desa
from hash_app.models import TableHash, ModifiedTableHash
from question_app.models import QuestionType, QuestionCategory, Question, Choice
from task_app.models import Task
from .serializers import (
    QuestionTypeSerializer,
    QuestionCategorySerializer,
    QuestionSerializer,
    ChoiceSerializer, TableHashSerializer, ProvinsiSerializer, KabupatenKotaSerializer, KecamatanSerializer,
    ModifiedTableHashSerializer, TaskSerializer, DesaSerializer
)

# class QuestionTypeViewSet(viewsets.ModelViewSet):
#     queryset = QuestionType.objects.all()
#     serializer_class = QuestionTypeSerializer
#     permission_classes = [IsAuthenticated]

class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

class QuestionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    permission_classes = [AllowAny]

class QuestionCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuestionCategory.objects.all()
    serializer_class = QuestionCategorySerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

class ChoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    # permission_classes = [IsAuthenticated]

    permission_classes = [AllowAny]

# nama_aplikasi_anda/views.py
from rest_framework import viewsets
from fitur_app.models import CheckupCategory, Feature
from .serializers import CheckupCategorySerializer, FeatureSerializer

class CheckupCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CheckupCategory.objects.all()
    serializer_class = CheckupCategorySerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

class TableHashViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TableHash.objects.all().order_by('model_name', '-last_updated') # Mengurutkan data
    serializer_class = TableHashSerializer
    permission_classes = [AllowAny]


class ProvinsiViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Provinsi.objects.all()
    serializer_class = ProvinsiSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

class KabupatenKotaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KabupatenKota.objects.all()
    serializer_class = KabupatenKotaSerializer
    permission_classes = [AllowAny]

class KecamatanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Kecamatan.objects.all()
    serializer_class = KecamatanSerializer
    permission_classes = [AllowAny]

class DesaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Desa.objects.all()
    serializer_class = DesaSerializer
    permission_classes = [AllowAny]



class ModifiedTableHashViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModifiedTableHash.objects.all()
    serializer_class = ModifiedTableHashSerializer

    # Jika Anda ingin API ini bisa diakses publik tanpa autentikasi, gunakan:
    permission_classes = [AllowAny]
