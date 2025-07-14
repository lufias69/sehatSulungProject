# urls.py
from django.urls import path
from . import views
app_name = 'checkup_app'
urlpatterns = [
    # path('create/', views.checkup_group_create, name='checkup_group_create'),
    path('', views.checkup_group_list, name='checkup_group_list'),
    path('#/<int:group_id>/', views.checkup_group_detail, name='checkup_group_detail'),

    path('select_category/', views.select_category, name='select_category'),
    path('create/<int:kategori_id>/', views.checkup_group_create, name='checkup_group_create'),
    path('#/<int:group_id>/edit/', views.checkup_group_edit, name='checkup_group_edit'),
    path('#/<int:group_id>/delete/', views.checkup_group_delete, name='checkup_group_delete'),
]
