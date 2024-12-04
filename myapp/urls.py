from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import ProductViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

# Define the URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
]
