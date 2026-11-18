"""Демонстрация ORM через manage.py shell, временные проверки откатываются."""

from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import IntegrityError, connection, transaction
from django.test.utils import CaptureQueriesContext
from news.models import Comment, News
from PIL import Image, ImageDraw


def run_demo():
    """Показывает CRUD и проверки, затем добавляет повторно используемые примеры."""
    # Каждый этап проверяет фактическое состояние. Временные строки не сохраняются.
    with transaction.atomic():
        print("1. CREATE: конструктор и save()")
        first = Comment(user_name="Первый", email="first@example.com", text="Пример")
        assert first.pk is None
        first.full_clean()
        first.save()
        assert first.pk == first.id and first.created_at is not None
        print("После save(): pk назначен, rating =", first.rating)

        second = Comment()
        second.user_name = "Второй"
        second.email = "second@example.com"
        second.text = "Еще пример"
        second.rating = 1
        second.is_moderated = True
        second.full_clean()
        second.save()
        third = Comment.objects.create(
            user_name="Третий",
            email="third@example.com",
            text="Еще пример",
            rating=5,
            is_moderated=True,
        )
        ids = [first.pk, second.pk, third.pk]
        comments = Comment.objects.filter(pk__in=ids)
        assert comments.count() == 3 and not first.is_moderated
        print("Три способа создания: 3 записи, границы рейтинга 1 и 5 сохранены")

        print("2. READ: all(), filter(), exclude(), get()")
        assert set(ids).issubset(
            set(Comment.objects.all().values_list("pk", flat=True))
        )
        approved = list(
            comments.filter(is_moderated=True).values_list("user_name", flat=True)
        )
        assert set(approved) == {"Второй", "Третий"}
        assert comments.exclude(is_moderated=True).get().pk == first.pk
        assert Comment.objects.get(pk=first.pk).text == "Пример"
        print("Прошли модерацию:", approved)
        print(
            "exclude(is_moderated=True):",
            list(
                comments.exclude(is_moderated=True).values_list("user_name", flat=True)
            ),
        )

        # QuerySet строится без SQL. Первое вычисление выполняет SELECT.
        with CaptureQueriesContext(connection) as queries:
            lazy = comments.filter(rating__gte=3)
            assert len(queries) == 0
            rows = list(lazy)
            assert len(queries) == 1 and len(rows) == 2
            list(lazy)
            assert len(queries) == 1
        print("Ленивый QuerySet: до list() 0 запросов, после 1, повторно 1")
        print("SQL:", queries[0]["sql"])

        print("3. UPDATE: изменение полей и повторный save()")
        created = first.created_at
        first.text = "Обновленный комментарий"
        first.is_moderated = True
        first.rating = 4
        first.full_clean()
        first.save()
        first.refresh_from_db()
        assert first.text == "Обновленный комментарий" and first.rating == 4
        assert (
            first.created_at == created
            and comments.filter(is_moderated=True).count() == 3
        )
        print("Обновление подтверждено чтением из базы, created_at сохранено")

        print("4. DELETE: удаление объекта")
        deleted_pk = third.pk
        third.delete()
        assert not Comment.objects.filter(pk=deleted_pk).exists()
        assert comments.count() == 2
        print("Удаленный объект отсутствует, осталось 2 временных комментария")

        print("5. Ошибки валидации и поиска")
        for field, value in [
            ("rating", 0),
            ("rating", 6),
            ("rating", None),
            ("email", "invalid"),
            ("text", ""),
            ("user_name", ""),
            ("user_name", "a" * 101),
        ]:
            invalid = Comment(
                user_name="Проверка", email="valid@example.com", text="Текст"
            )
            setattr(invalid, field, value)
            try:
                invalid.full_clean()
            except ValidationError as error:
                assert field in error.message_dict
                print(field, repr(value), "-> ValidationError")
            else:
                raise AssertionError((field, value))
        for value in (0, 6):
            try:
                with transaction.atomic():
                    comments.update(rating=value)
            except IntegrityError:
                assert comments.filter(rating__lt=1).count() == 0
                assert comments.filter(rating__gt=5).count() == 0
                print(
                    "update(rating=",
                    value,
                    ") -> IntegrityError, данные сохранены",
                    sep="",
                )
            else:
                raise AssertionError(value)
        try:
            Comment.objects.get(pk=deleted_pk)
        except Comment.DoesNotExist:
            print("get удаленной записи -> DoesNotExist")
        else:
            raise AssertionError("Ожидалась ошибка отсутствующего объекта")
        try:
            comments.get()
        except Comment.MultipleObjectsReturned:
            print("get нескольких записей -> MultipleObjectsReturned")
        else:
            raise AssertionError("Ожидалась ошибка неоднозначного поиска")

        print("6. Практическая модель News")
        news = News(title="Временная новость")
        news.full_clean()
        news.save()
        before_update = news.updated_at
        news.content = "Обновленный текст"
        news.save()
        news.refresh_from_db()
        assert news.content == "Обновленный текст" and news.updated_at > before_update
        assert news.is_published and not news.photo and str(news) == news.title
        news.delete()
        print("News: создание, чтение, обновление updated_at и удаление выполнены")
        transaction.set_rollback(True)
    print("Временные CRUD-сценарии отменены одной транзакцией")

    # Эти примеры остаются в базе для самостоятельного изучения через shell.
    for name, rating, moderated in [
        ("Анна", 5, True),
        ("Борис", 1, True),
        ("Вера", 3, False),
    ]:
        item, _ = Comment.objects.get_or_create(
            email=f"demo-{rating}@example.com",
            user_name=name,
            defaults={
                "text": f"Учебный комментарий: {name}",
                "rating": rating,
                "is_moderated": moderated,
            },
        )
        item.full_clean()
    article, _ = News.objects.get_or_create(
        title="Лабораторная 2: модели Django",
        defaults={"content": "Пример новости с изображением"},
    )
    if not article.photo:
        image = Image.new("RGB", (640, 240), "#17324d")
        draw = ImageDraw.Draw(image)
        draw.text((36, 94), "Django / Models / CRUD", fill="white", font_size=36)
        data = BytesIO()
        image.save(data, format="PNG")
        article.photo.save("django-models.png", ContentFile(data.getvalue()))
    assert article.photo.storage.exists(article.photo.name)
    print("7. Данные для самостоятельной работы")
    print(
        list(
            Comment.objects.order_by("pk").values("user_name", "rating", "is_moderated")
        )
    )
    print(
        "Модерированные:",
        list(
            Comment.objects.filter(is_moderated=True).values_list(
                "user_name", flat=True
            )
        ),
    )
    print("Фото:", article.photo.url)
    print("Все сценарии ORM пройдены")


run_demo()
