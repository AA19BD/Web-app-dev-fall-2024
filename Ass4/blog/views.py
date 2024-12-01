from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializerV1, CommentSerializerV1, PostSerializerV2, CommentSerializerV2
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostViewSetV1(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializerV1
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSetV1(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializerV1
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(post=post, author=self.request.user)


class PostViewSetV2(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializerV2
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSetV2(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializerV2
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(post=post, author=self.request.user)
