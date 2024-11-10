from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published_date__isnull=False)

    def by_author(self, author_name):
        return self.get_queryset().filter(author__username=author_name)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    published_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # New image field

    objects = models.Manager()
    published_posts = PublishedPostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100)
    posts = models.ManyToManyField('Post', related_name='categories')

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', db_index=True)
    author = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
