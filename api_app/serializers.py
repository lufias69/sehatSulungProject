# nama_aplikasi_anda/serializers.py
from rest_framework import serializers

from alamat_app.models import Provinsi, KabupatenKota, Kecamatan
from fitur_app.models import CheckupCategory, Feature
from hash_app.models import TableHash, ModifiedTableHash
from question_app.models import QuestionType, QuestionCategory, Question, Choice
from task_app.models import Task


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__' # Mengambil semua field dari model

class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class CheckupCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckupCategory
        fields = '__all__' # Mengambil semua field dari model

class FeatureSerializer(serializers.ModelSerializer):
    # Untuk menampilkan detail kategori di dalam fitur
    kategori = CheckupCategorySerializer(read_only=True)

    class Meta:
        model = Feature
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    # Untuk menampilkan detail choices di dalam pertanyaan
    choices = ChoiceSerializer(many=True, read_only=True)
    feature = FeatureSerializer(read_only=True)
    # Untuk menampilkan detail question_type dan category
    question_type = QuestionTypeSerializer(read_only=True)
    category = QuestionCategorySerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__' # Akan mencakup choices, question_type, dan category karena di-override di atas


class TableHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableHash
        fields = '__all__' # Ini akan menyertakan 'model_name', 'table_hash', dan 'last_updated'
        read_only_fields = ['last_updated'] # Field ini akan otomatis diisi Django


class ProvinsiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provinsi
        fields = '__all__' # Atau tentukan field yang ingin Anda expose: ['id', 'nama']

class KabupatenKotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KabupatenKota
        fields = '__all__'

class KecamatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kecamatan
        fields = '__all__'

class ModifiedTableHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifiedTableHash
        fields = '__all__' # Ini akan mengekspos semua field dari model
        # Atau Anda bisa spesifikkan field yang ingin Anda tampilkan:
        # fields = ['id', 'model_name', 'table_hash', 'last_updated', 'content_hash']
        read_only_fields = ['model_name', 'table_hash', 'last_updated', 'content_hash'] # Opsional, untuk menegaskan read-only

class TaskSerializer(serializers.ModelSerializer):
    # features = serializers.PrimaryKeyRelatedField(queryset=Feature.objects.all(), many=True)
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'task_duration', 'features', 'created_at']
