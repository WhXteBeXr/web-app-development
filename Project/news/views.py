"""Контроллер списка новостей и простая страница проверки маршрутов."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe

from .models import News


@require_safe
def index(request: HttpRequest) -> HttpResponse:
    """Передает новости в HTML-шаблон в порядке, заданном моделью."""
    # Запрос вычислится при обходе news в шаблоне, HTML в Python не собираем.
    context = {"news": News.objects.all(), "title": "Список новостей"}
    return render(request, "news/index.html", context)


@require_safe
def test(request: HttpRequest) -> HttpResponse:
    """Возвращает HTML-заголовок для проверки вложенного маршрута."""
    # HttpResponse задает тип text/html, поэтому браузер отображает заголовок.
    return HttpResponse("<h1>Тестовая страница</h1>")
