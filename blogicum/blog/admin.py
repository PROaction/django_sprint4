from django.contrib import admin

from blog.models import Category, Comment, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Location)
class LocationAmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
