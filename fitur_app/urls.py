# fitur_app/urls.py

from django.urls import path
from . import views
from checkup_app.views import checkup_category_update


app_name = 'fitur_app'
urlpatterns = [
    path('detail/<int:pk>/', views.feature_detail, name='feature_detail'),
    path('', views.view_features, name='view_features'),
    path('create/', views.create_feature, name='create_feature'),
    path('edit/<int:pk>/', views.edit_feature, name='edit_feature'),
    path('delete/<int:pk>/', views.delete_feature, name='delete_feature'),
    # URL untuk create question dan fitur lainnya

    path('categories/', views.checkup_category_list, name='checkup_category_list'),
    path('categories/create/', views.checkup_category_create, name='checkup_category_create'),
    path('categories/update/<int:category_id>/', checkup_category_update, name='checkup_category_update'),
    path('categories/delete/<int:category_id>/', views.checkup_category_delete, name='checkup_category_delete'),
]

