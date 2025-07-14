# question_app/urls.py

from django.urls import path
from . import views

app_name = 'question_app'  # Menetapkan namespace untuk aplikasi ini

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, FeatureViewSet, QuestionTypeViewSet, QuestionCategoryViewSet

# Membuat router dan mendaftarkan viewsets
router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'features', FeatureViewSet)
router.register(r'question-types', QuestionTypeViewSet)
router.register(r'question-categories', QuestionCategoryViewSet)


urlpatterns = [
    # path('create/', views.create_question, name='create_question'),
    # path('create/', views.add_update_delete_question, name='add_update_delete_question'),
    path('create/', views.create_question, name='create_question'),
    # path('edit/<int:pk>/', views.add_update_delete_question, name='edit_question'),
    # path('edit/<int:feature_id>/<int:question_id>/', views.add_update_delete_question, name='edit_question'),
    path('edit/<int:feature_id>/<int:question_id>/', views.edit_question, name='edit_question'),
    # path('delete/<int:pk>/', views.add_update_delete_question, name='delete_question'),
    path('delete/<int:feature_id>/<int:question_id>/', views.delete_question, name='delete_question'),
    # path('create/question_type/', views.create_question_type, name='create
    # _question_type'),
    # path('create/question_category/', views.create_question_category, name='create_question_category'),
    # path('edit/<int:pk>/', views.edit_question, name='edit_question'),
    # path('delete/<int:pk>/', views.delete_question, name='delete_question'),
    path('detail/<int:pk>/', views.question_detail, name='question_detail'),  # URL untuk detail pertanyaan
    path('', views.view_question_type_category, name='view_question_type_category'),
    path('create/question_type/', views.create_question_type, name='create_question_type'),
    path('create/question_category/', views.create_question_category, name='create_question_category'),
    path('edit/question_type/<int:pk>/', views.edit_question_type, name='edit_question_type'),
    path('edit/question_category/<int:pk>/', views.edit_question_category, name='edit_question_category'),
    path('delete/question_type/<int:pk>/', views.delete_question_type, name='delete_question_type'),
    path('delete/question_category/<int:pk>/', views.delete_question_category, name='delete_question_category'),
    path('api/', include(router.urls)),
]
