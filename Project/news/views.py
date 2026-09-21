from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def index(request) -> HttpResponse:
    print(request)
    return HttpResponse("Hello World")


@require_GET
def test(request) -> HttpResponse:
    return HttpResponse("<h1>Test page!</h1>")
