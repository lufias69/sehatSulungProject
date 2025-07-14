# task_app/forms.py

from django import forms
from .models import Task
from fitur_app.models import Feature  # Pastikan untuk mengimpor Feature

# task_app/forms.py

from django import forms
from .models import Task
from fitur_app.models import Feature  # Pastikan untuk mengimpor Feature

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'task_duration', 'features']  # Menambahkan 'features' sebagai field

    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task name'}))
    task_duration = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter task duration in days'}))
    features = forms.ModelMultipleChoiceField(queryset=Feature.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))


# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['name', 'task_duration', 'feature']  # Menentukan field yang akan dimasukkan dalam form
#
#     name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task name'}))
#     task_duration = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter task duration in days'}))
#     feature = forms.ModelChoiceField(queryset=Feature.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
