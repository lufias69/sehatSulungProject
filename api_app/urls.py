# nama_aplikasi_anda/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    QuestionTypeViewSet,
    QuestionCategoryViewSet,
    QuestionViewSet,
    ChoiceViewSet, CheckupCategoryViewSet, FeatureViewSet, TableHashViewSet, ProvinsiViewSet, KabupatenKotaViewSet,
    KecamatanViewSet, ModifiedTableHashViewSet, TaskViewSet
)

router = DefaultRouter()
router.register(r'question-types', QuestionTypeViewSet)
router.register(r'question-categories', QuestionCategoryViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'checkup-categories', CheckupCategoryViewSet)
router.register(r'features', FeatureViewSet)
router.register(r'table-hashes', TableHashViewSet)
router.register(r'provinsi', ProvinsiViewSet)
router.register(r'kabupaten-kota', KabupatenKotaViewSet)
router.register(r'kecamatan', KecamatanViewSet)
router.register(r'modified-table-hashes', ModifiedTableHashViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
