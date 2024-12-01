from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'published_date']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # Nested serializer for comments

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'published_date', 'image', 'comments']