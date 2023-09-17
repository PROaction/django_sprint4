from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class TemplateAboutView(TemplateView):
    template_name = 'pages/about.html'

class TemplateRulesView(TemplateView):
    template_name = 'pages/rules.html'

def about(request: HttpRequest) -> HttpResponse:
    """View-функция для инфо."""
    template = 'pages/about.html'
    return render(request, template)


def rules(request: HttpRequest) -> HttpResponse:
    """View-функция для правил."""
    template = 'pages/rules.html'
    return render(request, template)
