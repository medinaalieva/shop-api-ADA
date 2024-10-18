from rest_framework.routers import DefaultRouter

from django.urls import path, include

from apps.product.views import ProductViewSet

router = DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    path('', include(router.urls))
]
