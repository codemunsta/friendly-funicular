"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
# from users.custom_authentication import CustomAuthentication

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="BlackShakara",
        default_version="1.0.1",
        description="Backend documentation for BlackShakara",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="click2bundi@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        AllowAny,
    ],
    authentication_classes=[TokenAuthentication]
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('backend/admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
