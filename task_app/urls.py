# task_app/urls.py

from django.urls import path
from . import views
app_name = 'task_app'
urlpatterns = [
    path('task-list/', views.task_list, name='task_list'),
    # path('answer-task/<int:task_id>/', views.answer_task, name='answer_questions'),
    path('create/', views.create_task, name='create_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),  # Halaman edit task
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),  # Halaman konfirmasi delete task
    path('', views.checkup_group_list, name='checkup_group_list'),
]
