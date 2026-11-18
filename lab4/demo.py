"""Примеры связей для лабораторной 4, запуск через manage.py shell."""

from django.db import transaction
from django.db.models.deletion import ProtectedError
from news.models import Author, Book, Category, News

# Повторный запуск сохраняет уже существующие примеры и пользовательские правки.
category, _ = Category.objects.get_or_create(title="Учебные материалы")
News.objects.filter(
    category__isnull=True,
    title__in=(
        "Лабораторная 2: модели Django",
        "Шаблоны Django",
        "Настройка административной панели",
    ),
).update(category=category)
pushkin, _ = Author.objects.get_or_create(
    first_name="Александр",
    last_name="Пушкин",
    defaults={"biography": "Русский поэт и писатель."},
)
tolstoy, _ = Author.objects.get_or_create(
    first_name="Лев",
    last_name="Толстой",
    defaults={"biography": "Русский писатель."},
)
for title, year, isbn, author in [
    ("Евгений Онегин", 1833, "9785000000001", pushkin),
    ("Капитанская дочка", 1836, "9785000000002", pushkin),
    ("Война и мир", 1869, "9785000000003", tolstoy),
]:
    book, _ = Book.objects.get_or_create(
        isbn=isbn,
        defaults={"title": title, "publication_year": year, "author": author},
    )
    book.full_clean()
print("author.books:", list(pushkin.books.values_list("title", flat=True)))
print("Новости категории:", list(category.news.values_list("title", flat=True)))

# Удаление проверяется только на временных строках с полным откатом.
with transaction.atomic():
    temporary = Author.objects.create(first_name="Временный", last_name="Автор")
    book = Book.objects.create(
        title="Проверка CASCADE",
        publication_year=2026,
        isbn="demo-cascade-only",
        author=temporary,
    )
    pk = book.pk
    temporary.delete()
    assert not Book.objects.filter(pk=pk).exists()
    print("CASCADE: удаление автора удалило его временную книгу")
    try:
        category.delete()
    except ProtectedError:
        print("PROTECT: категория с новостями защищена")
    else:
        print("Категория не содержала новостей, удаление допустимо")
    transaction.set_rollback(True)
print("Постоянные данные сохранены, временные изменения отменены")
