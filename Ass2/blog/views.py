from django.http import JsonResponse
from .models import Post


def index(request):
    posts = Post.objects.all()
    posts_data = [{'id': post.id, 'title': post.title} for post in posts]
    return JsonResponse(posts_data, safe=False)  # safe=False allows non-dict objects
