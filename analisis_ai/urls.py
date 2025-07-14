from django.urls import path
from . import views
app_name = 'analisis_ai'
urlpatterns = [
    path('health_prediction/<int:session_id>/', views.make_health_prediction, name='make_health_prediction'),
]
