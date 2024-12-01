from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSetV1, PostViewSetV2, CommentViewSetV1, CommentViewSetV2

router = DefaultRouter()
router.register(r'v1/posts', PostViewSetV1, basename='post-v1')
router.register(r'v2/posts', PostViewSetV2, basename='post-v2')
router.register(r'v1/posts/(?P<post_id>\d+)/comments', CommentViewSetV1, basename='post-comments-v1')  # Provide basename
router.register(r'v2/posts/(?P<post_id>\d+)/comments', CommentViewSetV2, basename='post-comments-v2')

urlpatterns = [
    path('', include(router.urls)),
]
