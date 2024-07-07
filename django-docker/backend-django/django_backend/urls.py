"""
URL configuration for django_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)


urlpatterns = [
    path("api/admin/", admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/board/', include('board.urls')),

    path("api/docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("api/docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),

    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui-default"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
