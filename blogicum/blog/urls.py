from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/<int:id>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('profile/<slug:username_slug>/', views.ProfileDetailView.as_view(), name='profile'),
    path('edit_profile/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('category/<slug:category_slug>/', views.CategoryListView.as_view(),
         name='category_posts'),
]
