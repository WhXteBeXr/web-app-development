"""Маршруты приложения после удаления общего префикса news/."""

from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.test, name="test"),
    path("<int:pk>/", views.detail, name="detail"),
]
