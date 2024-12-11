from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import CustomerViewSet, OrderViewSet

# Initialize a global router for other app-specific views
router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')

# Define global URL patterns
urlpatterns = [
    path('api/', include(router.urls)),  # Includes customer and order routes
    path('api/', include('myapp.urls')),  # Includes product routes and JWT token endpoints
]
