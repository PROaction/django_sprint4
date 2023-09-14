from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import path, include, reverse_lazy
from django.views.generic import CreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
            'auth/registration/',
            CreateView.as_view(
                template_name='registration/registration_form.html',
                form_class=UserCreationForm,
                success_url=reverse_lazy('blog:index'),
            ),
            name='registration',
        ),
]

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
