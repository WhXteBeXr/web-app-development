# Лабораторная работа № 2 - модели и CRUD

Продолжение общего сайта в `Project/`. Практическая модель `News`, индивидуальный вариант 3 - `Comment`. Уровни сложности в методичке не выделены.

Команды выполнять из корня репозитория:

```bash
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python Project/manage.py migrate
python Project/manage.py shell < lab2/demo.py
python Project/manage.py check
python Project/manage.py runserver 127.0.0.1:8002
```

`demo.py` запускается внутри Django shell. Он проверяет CRUD, фильтрацию и ограничения, откатывает временные строки и оставляет три учебных комментария и новость с изображением. Повторный запуск не дублирует исходные учебные записи. Пользовательские данные не очищаются.

Для самостоятельных запросов:

```bash
python Project/manage.py shell
```

```python
from news.models import Comment, News
Comment.objects.all()
Comment.objects.filter(is_moderated=True)
Comment.objects.exclude(is_moderated=True)
News.objects.all()
```

Адреса страниц: `http://127.0.0.1:8002/news/` и `/news/test/`. В shell выражение `News.objects.get(title="Лабораторная 2: модели Django").photo.url` покажет адрес изображения, которое можно открыть в браузере.

`Project/db.sqlite3` и `Project/uploads/` создаются локально и исключены из Git. Их можно воспроизвести командами миграции и демонстрации. Каталог `lab2/media/` содержит материалы отчета, а не загружаемые изображения сайта.

- [Отчет](report.md)
- [Подробная памятка](defense.md)
- [Вывод ORM](media/orm-demo.txt)
- [Результаты HTTP](media/http-scenarios.json)
