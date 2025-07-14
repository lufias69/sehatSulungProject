from django.urls import path
from . import views
from .views import feedback_view

app_name = 'session_app'
urlpatterns = [
    # URL untuk mengakses API fitur dan pertanyaan
    path('questions-by-feature/<int:pk>/', views.get_questions_by_feature, name='get_questions_by_feature'),
    path('feature/<int:pk>/answer/<int:checkup_group_id>/', views.answer_questions, name='answer_questions'),
    path('feedback/<int:checkup_group_id>/<int:session_id>/', views.feedback_view, name='feedback'),

]


