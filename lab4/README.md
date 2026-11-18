# Лабораторная работа № 4 - связи моделей

Вариант 3 «Библиотека: книги и авторы» и общая практическая часть с категориями новостей. В методичке нет деления на уровни.

Из корня репозитория:

```bash
source .venv/bin/activate
python Project/manage.py migrate
python Project/manage.py shell < lab2/demo.py
python Project/manage.py shell < lab3/demo.py
python Project/manage.py shell < lab4/demo.py
python Project/manage.py runserver 127.0.0.1:8002
```

Для первого входа в `/admin/` нужно создать свою учетную запись через `python Project/manage.py createsuperuser`. Уже существующую учетную запись можно использовать повторно.

- `/admin/news/author/` - авторы, их биографии и необязательные фотографии.
- `/admin/news/book/` - книги, авторы, ISBN, фильтры и редактирование года в списке.
- `/admin/news/category/` - категории новостей.
- `/admin/news/news/` - категории, фильтры и редактирование публикации в списке.
- `/news/` - лента с названием категории.

`demo.py` добавляет двух авторов, три книги и категорию. Он связывает с ней только учебные новости предыдущих работ, у которых категория еще не задана. Учебные ISBN условные и не являются библиографическим каталогом реальных изданий.

Временное удаление автора проверяет CASCADE, попытка удаления категории - PROTECT. Обе операции в сценарии откатываются, постоянные данные сохраняются. Для проверки вручную создавайте отдельные пробные записи: удаление автора в админке действительно удалит все его книги после подтверждения.

В shell:

```python
from news.models import Author, Book, Category
pushkin = Author.objects.get(first_name="Александр", last_name="Пушкин")
pushkin.books.all()
Book.objects.select_related("author")
Category.objects.get(title="Учебные материалы").news.all()
```

[Отчет](report.md), [памятка](defense.md), [42 проверенных сценария](media/scenarios.json).
