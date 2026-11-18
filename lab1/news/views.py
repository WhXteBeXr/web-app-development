"""Два простых контроллера без шаблонов и обращения к базе данных."""

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_safe


@require_safe
def index(request: HttpRequest) -> HttpResponse:
    """Возвращает приветствие на главной странице приложения news."""
    # Разрешаем чтение через GET и HEAD. Тело ответа задаем напрямую.
    return HttpResponse("Hello world")


@require_safe
def test(request: HttpRequest) -> HttpResponse:
    """Возвращает HTML-заголовок для проверки вложенного маршрута."""
    # HttpResponse задает тип text/html, поэтому браузер отображает заголовок.
    return HttpResponse("<h1>Тестовая страница</h1>")
