from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def about(request: HttpRequest) -> HttpResponse:
    """View-функция для инфо."""
    template = 'pages/about.html'
    return render(request, template)


def rules(request: HttpRequest) -> HttpResponse:
    """View-функция для правил."""
    template = 'pages/rules.html'
    return render(request, template)
