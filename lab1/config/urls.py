"""Корневой маршрутизатор передает адреса news/ приложению."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Остаток пути, например test/, разбирается внутри news.urls.
    path("news/", include("news.urls")),
]
