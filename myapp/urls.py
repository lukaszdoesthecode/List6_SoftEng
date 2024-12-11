from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import ProductViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Initialize the router and register views
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

# Define app-specific URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Router handles registered views
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT Token endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT Token refresh endpoint
]
