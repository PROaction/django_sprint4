from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.list import MultipleObjectMixin

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post

ELEMS_PER_PAGE = 10


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = ELEMS_PER_PAGE

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


class CategoryDetailView(DetailView, MultipleObjectMixin):
    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'
    paginate_by = ELEMS_PER_PAGE

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().is_published:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        object_list = Post.objects.select_related(
            'category'
        ).filter(is_published=True,
                 category__is_published=True,
                 category__slug=self.kwargs['category_slug'],
                 pub_date__lte=datetime.now(),
                 )
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        print(self.get_object().pub_date.timestamp())
        print(datetime.now().timestamp())
        if self.get_object().author != request.user:
            if (self.get_object().pub_date.timestamp()
                    > datetime.now().timestamp()
                    or not self.get_object().is_published
                    or not self.get_object().category.is_published):
                raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create_post.html'

    def dispatch(self, request, *args, **kwargs):
        if (self.get_object().author != request.user
                and not request.user.is_superuser):
            return redirect(
                'blog:post_detail',
                post_id=self.kwargs['post_id']
            )
        get_object_or_404(Post, pk=kwargs['post_id'], author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.request.user.username])


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/create_post.html'

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.request.user.username])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    pk_url_kwarg = 'post_id'
    allow_empty = False

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.kwargs['post_id']])


class ProfileDetailView(DetailView, MultipleObjectMixin):
    User = get_user_model()
    model = User
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username_slug'
    context_object_name = 'profile'
    paginate_by = ELEMS_PER_PAGE

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username_slug'])

    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(
            author__username=self.kwargs['username_slug'])
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    User = get_user_model()
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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'comment'
    page_obj = None

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_pk']

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.kwargs['post_pk']])


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    allow_empty = False
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            print(self.get_object().author, request.user)
            print('Перенаправление')
            return redirect('blog:post_detail', post_id=self.kwargs['post_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.kwargs['post_pk']])


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.kwargs['post_pk']])
