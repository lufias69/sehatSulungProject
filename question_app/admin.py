# question_app/admin.py

from django.contrib import admin
from .models import QuestionType, QuestionCategory, Question

admin.site.register(QuestionType)
admin.site.register(QuestionCategory)
admin.site.register(Question)
