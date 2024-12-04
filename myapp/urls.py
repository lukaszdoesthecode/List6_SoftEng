from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductListView, ProductDetailView, ProductCreateView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

# Define the URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
    path('user/products/', ProductListView.as_view(), name='product_list'),
    path('user/products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('user/products/new/', ProductCreateView.as_view(), name='product_create'),
]
