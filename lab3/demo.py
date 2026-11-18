"""Учебные новости для просмотра шаблона, запуск через manage.py shell."""

from news.models import News

# Существующие записи сохраняются. Повторный запуск не создает дубли примеров.
for title, content, published in [
    (
        "Шаблоны Django",
        "Контроллер передает данные в контекст.\nШаблон формирует HTML-страницу.",
        True,
    ),
    (
        "Настройка административной панели",
        "В админке доступны добавление, изменение, поиск и удаление новостей.",
        False,
    ),
]:
    item, created = News.objects.get_or_create(
        title=title, defaults={"content": content, "is_published": published}
    )
    print("Создана" if created else "Уже существует", item.title)

print("Порядок новостей:", list(News.objects.values_list("title", flat=True)))
