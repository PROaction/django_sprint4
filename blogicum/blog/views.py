from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm
from .mixins import CommentMixin, PostMixin, PostsMixin
from .models import Category, Comment, Post, User


class IndexListView(PostsMixin, ListView):
    template_name = 'blog/index.html'


class CategoryListView(PostsMixin, ListView):
    template_name = 'blog/category.html'
    category_obj = None

    def get_queryset(self):
        self.category_obj = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
        )
        return super().get_queryset().filter(category=self.category_obj)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['category'] = self.category_obj
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post_obj = get_object_or_404(
            Post,
            pk=self.kwargs['post_id']
        )
        if post_obj.author != self.request.user:
            if (
                    not post_obj.is_published
                    or not post_obj.category.is_published
                    or post_obj.pub_date > timezone.now()
            ):
                raise Http404
        return post_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/create_post.html'

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, PostMixin, DeleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class ProfileListView(PostsMixin, ListView):
    template_name = 'blog/profile.html'
    current_user = None

    def get_queryset(self):
        self.current_user = get_object_or_404(
            User,
            username=self.kwargs['username_slug']
        )
        if self.request.user.username == self.kwargs['username_slug']:
            return self.all_posts().filter(
                author__username=self.kwargs['username_slug'],
            )
        else:
            return super().get_queryset().filter(
                author__username=self.kwargs['username_slug'],
            )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['profile'] = self.current_user
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
        return reverse('blog:profile', args=[self.request.user.username])


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = get_object_or_404(
            Post,
            pk=self.kwargs['post_pk']
        ).pk

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_pk']])


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pass
