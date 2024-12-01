from rest_framework import serializers
from .models import Post, Comment


class CommentSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'published_date']


class PostSerializerV1(serializers.ModelSerializer):
    comments = CommentSerializerV1(many=True, read_only=True)  # Nested serializer for comments

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'published_date', 'image', 'comments']


class CommentSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'published_date']


class PostSerializerV2(serializers.ModelSerializer):
    comments = CommentSerializerV2(many=True, read_only=True)  # Nested serializer for comments

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'published_date', 'image', 'comments']