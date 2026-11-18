"""Настройка списков, поиска и форм административной панели."""

from django.contrib import admin
from django.urls import reverse_lazy

from .models import Author, Book, Category, Comment, News

# Ссылка «Открыть сайт» ведет на ленту, поскольку корневой URL не зарегистрирован.
admin.site.site_url = reverse_lazy("news:index")


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Показывает поля новости и позволяет искать записи по заголовку и тексту."""

    list_display = (
        "id",
        "title",
        "category",
        "created_at",
        "updated_at",
        "is_published",
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    list_filter = ("category", "is_published")
    list_editable = ("is_published",)
    list_select_related = ("category",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Предоставляет в админке доступ к модели варианта 3 из второй работы."""

    list_display = ("id", "user_name", "rating", "is_moderated", "created_at")
    list_display_links = ("id", "user_name")
    search_fields = ("user_name", "email", "text")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Позволяет создавать категории и искать их по названию."""

    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Настраивает список авторов, поиск по имени, фамилии и биографии."""

    list_display = ("id", "last_name", "first_name")
    list_display_links = ("id", "last_name")
    search_fields = ("first_name", "last_name", "biography")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Выводит связанного автора и позволяет менять год в списке книг."""

    list_display = ("id", "title", "author", "publication_year", "isbn")
    list_display_links = ("id", "title")
    list_filter = ("author", "publication_year")
    list_editable = ("publication_year",)
    search_fields = ("title", "isbn", "author__first_name", "author__last_name")
    list_select_related = ("author",)
