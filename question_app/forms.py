# question_app/forms.py

from django import forms
from .models import Question, QuestionType, QuestionCategory, Choice

# question_app/forms.py

from django import forms
from .models import Question, QuestionType, QuestionCategory, Feature, Choice

# question_app/forms.py

# question_app/forms.py
#
# from django import forms
# from .models import Question, QuestionType, QuestionCategory, Feature

# fitur_app/forms.py

from django import forms
from .models import Question, QuestionType, QuestionCategory, Feature

# question_app/forms.py

from django import forms
from .models import Question, QuestionType, QuestionCategory, Feature

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['priority','question_text', 'question_type', 'category', 'is_mandatory', 'image']

    # Untuk menambahkan pilihan jika jenis pertanyaannya adalah Pilihan Ganda atau Centang
    # choices = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter choices here (one per line)'}), required=False)
    widgets = {
        'question_type': forms.Select(attrs={'id': 'question_type', 'class': 'form-control'}),
        'category': forms.Select(attrs={'id': 'category', 'class': 'form-control'}),
        'image': forms.HiddenInput(),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Menentukan queryset untuk dropdown agar datanya muncul
        self.fields['question_type'].queryset = QuestionType.objects.all()
        self.fields['category'].queryset = QuestionCategory.objects.all()


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question_text', 'question_type', 'category', 'feature', 'is_mandatory', 'image']
#
#     # Untuk menambahkan pilihan jika jenis pertanyaannya adalah Pilihan Ganda atau Centang
#     choices = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter choices here (one per line)'}), required=False)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Menentukan queryset untuk dropdown agar datanya muncul
#         self.fields['question_type'].queryset = QuestionType.objects.all()  # Menyediakan jenis pertanyaan
#         self.fields['category'].queryset = QuestionCategory.objects.all()  # Menyediakan kategori pertanyaan
#         self.fields['feature'].queryset = Feature.objects.all()  # Menyediakan fitur untuk pertanyaan


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question_text', 'question_type', 'category', 'feature', 'is_mandatory', 'image']
#
#     # Untuk menambahkan pilihan jika jenis pertanyaannya adalah Pilihan Ganda atau Centang
#     choices = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter choices here (one per line)'}), required=False)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Querysets untuk dropdown
#         self.fields['question_type'].queryset = QuestionType.objects.all()  # Menyediakan jenis pertanyaan
#         self.fields['category'].queryset = QuestionCategory.objects.all()  # Menyediakan kategori pertanyaan
#         self.fields['feature'].queryset = Feature.objects.all()  # Menyediakan fitur untuk pertanyaan


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question_text', 'question_type', 'category', 'feature', 'is_mandatory', 'image']
#
#     # Untuk menambahkan pilihan jika jenis pertanyaannya adalah Pilihan Ganda atau Centang
#     choices = forms.ModelMultipleChoiceField(
#         queryset=Choice.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Pilihan jenis pertanyaan (Essai, Pilihan Ganda, Centang)
#         self.fields['question_type'].queryset = QuestionType.objects.all()
#
#         # Pilihan kategori pertanyaan (Anak Bayi, Wanita Subur, dll)
#         self.fields['category'].queryset = QuestionCategory.objects.all()
#
#         # Pilihan fitur pertanyaan (Cek Stunting, Cek Tuberkulosis, dll)
#         self.fields['feature'].queryset = Feature.objects.all()


# question_app/forms.py

from django import forms
from .models import QuestionType

class QuestionTypeForm(forms.ModelForm):
    class Meta:
        model = QuestionType
        fields = ['name', 'description']


class QuestionCategoryForm(forms.ModelForm):
    class Meta:
        model = QuestionCategory
        fields = ['name', 'age','description']
