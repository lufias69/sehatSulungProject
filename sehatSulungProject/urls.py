"""
URL configuration for sehatSulungProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('question/', include('question_app.urls')),
    path('features/', include('fitur_app.urls')),
    path('media/', include('media_center_app.urls')),
    path('check/', include('checkup_app.urls')),
    path('alamat/', include('alamat_app.urls')),

    path('session/', include('session_app.urls')),
    path('task/', include('task_app.urls')),
    path('ai/', include('analisis_ai.urls')),
    path('accounts/', include('allauth.urls')),  # Include allauth URLs
    path('', RedirectView.as_view(pattern_name='task_app:checkup_group_list'), name='root_redirect'),
    path('api/', include('api_app.urls')),

]
