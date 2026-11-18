"""Модели практической части и индивидуального варианта 3."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    """Объединяет новости по теме, хранит название в одной отдельной таблице."""

    title = models.CharField("Категория", max_length=150, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("title", "pk")

    def __str__(self) -> str:
        """Возвращает название для списка выбора категории в админке."""
        return self.title


class News(models.Model):
    """Хранит новость, даты ее изменения и путь к необязательному изображению."""

    title = models.CharField("Заголовок", max_length=150)
    content = models.TextField("Содержание", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)
    # В базе хранится путь, содержимое изображения находится в MEDIA_ROOT.
    photo = models.ImageField("Изображение", upload_to="photos/%Y/%m/%d/", blank=True)
    is_published = models.BooleanField("Опубликована", default=True)
    # NULL сохраняет старые новости, blank разрешает прежние сценарии без категории.
    # Категорию с новостями удалить нельзя, произвольный default=id не задается.
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="news",
        null=True,
        blank=True,
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        # При одинаковых датах первичный ключ сохраняет однозначный порядок.
        ordering = ("-created_at", "-pk")

    def __str__(self) -> str:
        """Возвращает заголовок для понятного отображения объекта в shell."""
        return self.title


class Comment(models.Model):
    """Хранит автора, текст и состояние модерации комментария."""

    user_name = models.CharField("Имя пользователя", max_length=100)
    email = models.EmailField("Электронная почта")
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    is_moderated = models.BooleanField("Прошел модерацию", default=False)
    # Валидаторы дают понятную ошибку full_clean(), CHECK защищает саму базу.
    rating = models.PositiveSmallIntegerField(
        "Рейтинг", default=3, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        constraints = (
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name="comment_rating_1_to_5",
            ),
        )

    def __str__(self) -> str:
        """Возвращает автора и начало текста без переноса всей записи в вывод."""
        return f"{self.user_name}: {self.text[:50]}"


class Author(models.Model):
    """Хранит автора библиотеки индивидуального варианта 3."""

    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    biography = models.TextField("Биография", blank=True)
    photo = models.ImageField("Фото", upload_to="authors/%Y/%m/%d/", blank=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ("last_name", "first_name", "pk")

    def __str__(self) -> str:
        """Возвращает фамилию и имя для выбора автора книги."""
        return f"{self.last_name} {self.first_name}"


class Book(models.Model):
    """Связывает книгу с одним обязательным автором и уникальным ISBN."""

    title = models.CharField("Название", max_length=200)
    publication_year = models.PositiveSmallIntegerField(
        "Год издания", validators=[MinValueValidator(1), MaxValueValidator(9999)]
    )
    isbn = models.CharField("ISBN", max_length=17, unique=True)
    # Без автора книга не сохраняется. author.books дает обратный доступ.
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", verbose_name="Автор"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ("title", "pk")

    def __str__(self) -> str:
        """Возвращает название книги без дополнительного запроса автора."""
        return self.title
