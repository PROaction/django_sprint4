from django.urls import path, include

from . import views

app_name = 'blog'
posts_urls = [
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),
    path('<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),
    path('<int:post_pk>/comment/',
         views.CommentCreateView.as_view(),
         name='add_comment'),
    path('<int:post_pk>/edit_comment/<int:comment_pk>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),
    path('<int:post_pk>/delete_comment/<int:comment_pk>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),
]

urlpatterns = [
    path('posts/', include(posts_urls)),
    path('', views.IndexListView.as_view(), name='index'),
    path('profile/<slug:username_slug>/',
         views.ProfileListView.as_view(),
         name='profile'),
    path('edit_profile/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(),
         name='category_posts'),
]
