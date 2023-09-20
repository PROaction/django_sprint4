from blog.models import Comment, Post
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse


class PostMixin:
    model = Post
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.select_related(
            'category', 'author', 'location'
        ).order_by('-pub_date').annotate(comment_count=Count('comments'))


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_pk']])
