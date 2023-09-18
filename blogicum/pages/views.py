from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class TemplateAboutView(TemplateView):
    template_name = 'pages/about.html'

class TemplateRulesView(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def permission_denied(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)

def about(request: HttpRequest) -> HttpResponse:
    """View-функция для инфо."""
    template = 'pages/about.html'
    return render(request, template)


def rules(request: HttpRequest) -> HttpResponse:
    """View-функция для правил."""
    template = 'pages/rules.html'
    return render(request, template)
