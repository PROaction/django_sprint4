from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .forms import PostForm
from .models import Category, Post


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = 'id'
    paginate_by = 10


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.request.user.username])

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    allow_empty = False
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)




class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username_slug'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['profile'] = User.objects.get(username=self.kwargs['username'])
        context['page_obj'] = Post.objects.filter(author__username=self.kwargs['username_slug'])
        return context


class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'blog/user.html'
    slug_url_kwarg = 'username_slug'
    fields = [
        'first_name',
        'last_name',
        'email',
    ]

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.request.user.username])


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """View-функция для конкретнго поста."""
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_posts_from_bd().filter(
            pk=id,
            category__is_published=True,
        )
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """View-функция для конкретной категории."""
    template = 'blog/category.html'
    category = get_object_or_404(Category,
                                 slug=category_slug,
                                 is_published=True)
    posts = get_posts_from_bd().filter(
        category__slug=category_slug,
    )

    context = {'posts': posts,
               'category': category,
               }
    return render(request, template, context)


def index(request: HttpRequest) -> HttpResponse:
    """View-функция для главной страницы."""
    template = 'blog/index.html'
    posts = get_posts_from_bd().filter(
        category__is_published=True,
    )[:5]
    context = {'posts': posts}
    return render(request, template, context)


def get_posts_from_bd() -> QuerySet:
    """Базовое получение постов."""
    posts = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        pub_date__lte=datetime.now(),
    )

    return posts
