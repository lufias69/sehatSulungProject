# question_app/serializers.py
import json

from cloudinary.cache.responsive_breakpoints_cache import instance
from django.http import request
from rest_framework import serializers
from .models import Question, Feature, QuestionType, QuestionCategory, Choice


# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['id', 'question_text', 'question_type', 'category', 'is_mandatory', 'feature', 'image']
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_text']

class QuestionSerializer(serializers.ModelSerializer):
    choices_data = serializers.ListField(child=serializers.CharField(),  required=False) #write_only=True,

    class Meta:
        model = Question
        fields = ['id', 'priority','question_text', 'question_type', 'category', 'feature', 'choices_data', 'image']

    def get_choices(self, obj):
        return list(obj.choices.values_list('choice_text', flat=True))

    def create(self, validated_data):
        choices = validated_data.pop('choices_data', [])
        print(choices)
        question = Question.objects.create(**validated_data)
        for choice_text in choices:
            c= json.loads(choice_text)
            for ic in c:
                Choice.objects.create(question=question, choice_text=ic)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices_data', None)

        # ✅ Jika image tidak dikirim, jangan ubah instance.image
        if 'image' not in self.initial_data or not self.initial_data.get('image'):
            print("image tidak dikirim, tetap gunakan gambar lama")
        else:
            print("image dikirim")
            instance.image = validated_data.get('image')

        # ✅ Update semua field kecuali image
        for attr, value in validated_data.items():
            if attr != 'image':  # image sudah ditangani di atas
                setattr(instance, attr, value)

        instance.save()

        # ✅ Update pilihan
        if choices is not None:
            instance.choices.all().delete()
            for choice_text in choices:
                c = json.loads(choice_text)
                for ic in c:
                    Choice.objects.create(question=instance, choice_text=ic)
                # Choice.objects.create(question=instance, choice_text=choice_text)

        return instance

    # def update(self, instance, validated_data):
    #     choices = validated_data.pop('choices_data', None)
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #
    #     if choices is not None:
    #         # Hapus semua pilihan lama lalu tambahkan yang baru
    #         instance.choices.all().delete()
    #         for choice_text in choices:
    #             Choice.objects.create(question=instance, choice_text=choice_text)
    #
    #     return instance




class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name', 'description', 'image']

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ['id', 'name', 'description']




# question_app/serializers.py

class FeatureSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)  # Menambahkan pertanyaan terkait
    # questions = QuestionSerializer(instance, data=request.data, partial=True)

    class Meta:
        model = Feature
        fields = ['id', 'name', 'description', 'image', 'questions']

class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ['id', 'name', 'description', 'age', 'image']
