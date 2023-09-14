from django.contrib import admin

from blog.models import Location, Category, Post

admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Post)
