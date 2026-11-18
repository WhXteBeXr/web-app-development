"""Модели практической части и индивидуального варианта 3."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class News(models.Model):
    """Хранит новость, даты ее изменения и путь к необязательному изображению."""

    title = models.CharField("Заголовок", max_length=150)
    content = models.TextField("Содержание", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)
    # В базе хранится путь, содержимое изображения находится в MEDIA_ROOT.
    photo = models.ImageField("Изображение", upload_to="photos/%Y/%m/%d/", blank=True)
    is_published = models.BooleanField("Опубликована", default=True)

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
        constraints = (
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name="comment_rating_1_to_5",
            ),
        )

    def __str__(self) -> str:
        """Возвращает автора и начало текста без переноса всей записи в вывод."""
        return f"{self.user_name}: {self.text[:50]}"
