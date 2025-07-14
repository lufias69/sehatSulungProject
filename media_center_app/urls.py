from django.urls import path
from . import views

app_name = 'media_center_app'



urlpatterns = [
    path('', views.media_list, name='media_list'),
    path('upload/', views.media_upload, name='media_upload'),
]
