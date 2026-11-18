"""Настройка списков, поиска и форм административной панели."""

from django.contrib import admin
from django.urls import reverse_lazy

from .models import Comment, News

# Ссылка «Открыть сайт» ведет на ленту, поскольку корневой URL не зарегистрирован.
admin.site.site_url = reverse_lazy("news:index")


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Показывает поля новости и позволяет искать записи по заголовку и тексту."""

    list_display = ("id", "title", "created_at", "updated_at", "is_published")
    list_display_links = ("id", "title")
    search_fields = ("title", "content")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Предоставляет в админке доступ к модели варианта 3 из второй работы."""

    list_display = ("id", "user_name", "rating", "is_moderated", "created_at")
    list_display_links = ("id", "user_name")
    search_fields = ("user_name", "email", "text")
