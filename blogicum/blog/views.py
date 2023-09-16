from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import PostForm, CommentForm
from .models import Category, Post, Comment


User = get_user_model()

class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = 'id'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=datetime.now(),
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = Post.objects.select_related(
            'category'
        ).filter(is_published=True,
                 category__is_published=True,
                 pub_date__lte=datetime.now(),
                 )
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        context['comments'] = self.object.comments.select_related('author')
        return context


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create_post.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.request.user.username])


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = 'blog/create_post.html'

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
    template_name = 'blog/create_post.html'
    allow_empty = False

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.kwargs['pk']])


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username_slug'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = Post.objects.filter(author__username=self.kwargs['username_slug'])
        return context


class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = [
        'first_name',
        'last_name',
        'email',
    ]

    def get_object(self, queryset=None):
        return self.model.objects.get(username=self.request.user.username)

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.request.user.username])


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'comment'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_pk']

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.kwargs['post_pk']])


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    allow_empty = False
    pk_url_kwarg = 'comment_pk'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.kwargs['post_pk']])


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.kwargs['post_pk']])


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


