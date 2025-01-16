from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import ProductViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Initialize the router and register views
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

schema_view = get_schema_view(
openapi.Info(
title="Software engineering lab",
default_version="v1",
description="API documentation for the lab",
),
public=True,
permission_classes=(AllowAny,),
authentication_classes=[],
)

# Define app-specific URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Router handles registered views
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT Token endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT Token refresh endpoint
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
