# alamat_app/urls.py
from django.urls import path
from . import views

app_name = 'alamat_app'

urlpatterns = [
    path('kabupaten_kota/', views.get_kabupaten_kota, name='kabupaten_kota'),
    path('kecamatan/', views.get_kecamatan, name='kecamatan'),
    path('desa/', views.get_desa, name='desa'),
    path('submit/', views.submit_alamat, name='submit_alamat'),

    path('', views.provinsi_list, name='provinsi_list'),
    path('provinsi/edit/<int:provinsi_id>/', views.edit_provinsi, name='edit_provinsi'),
    path('provinsi/delete/<int:provinsi_id>/', views.delete_provinsi, name='delete_provinsi'),
    path('provinsi/add/', views.add_provinsi, name='add_provinsi'),
    path('kabupaten/<int:provinsi_id>/', views.kabupaten_list, name='kabupaten_list'),
    path('kabupaten/add/<int:provinsi_id>/', views.add_kabupaten, name='add_kabupaten'),
    path('kabupaten/edit/<int:kabupaten_id>/', views.edit_kabupaten, name='edit_kabupaten'),
    path('kabupaten/delete/<int:kabupaten_id>/', views.delete_kabupaten, name='delete_kabupaten'),
    path('kecamatan/<int:kabupaten_id>/', views.kecamatan_list, name='kecamatan_list'),
    path('kecamatan/add/<int:kabupaten_id>/', views.add_kecamatan, name='add_kecamatan'),
    path('kecamatan/edit/<int:kecamatan_id>/', views.edit_kecamatan, name='edit_kecamatan'),
    path('kecamatan/delete/<int:kecamatan_id>/', views.delete_kecamatan, name='delete_kecamatan'),
    path('desa/<int:kecamatan_id>/', views.desa_list, name='desa_list'),
    path('desa/add/<int:kecamatan_id>/', views.add_desa, name='add_desa'),
    path('desa/edit/<int:desa_id>/', views.edit_desa, name='edit_desa'),
    path('desa/delete/<int:desa_id>/', views.delete_desa, name='delete_desa'),
    path('desa/search/', views.desa_search, name='desa_search'),
    path('desa/<int:desa_id>/select/', views.select_desa, name='select_desa'),
    path('filter-kabupaten/', views.filter_kabupaten_by_provinsi, name='filter_kabupaten'),
    path('filter-kecamatan/', views.filter_kecamatan_by_kabupaten, name='filter_kecamatan'),
    path('filter-desa/', views.filter_desa_by_kecamatan, name='filter_desa'),
]
