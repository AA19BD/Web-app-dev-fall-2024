from django.contrib import admin
from .models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('published_date', 'author')
    ordering = ('-published_date',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'published_date')
    search_fields = ('author', 'content')
    list_filter = ('published_date',)


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
