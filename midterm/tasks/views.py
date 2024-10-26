import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Task


def task_list(request):
    tasks = Task.objects.all().values()
    return JsonResponse(list(tasks), safe=False)


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return JsonResponse({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at,
        'completed': task.completed,
    })


@csrf_exempt
def task_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            task = Task.objects.create(title=title, description=description)
            return JsonResponse({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'created_at': task.created_at,
                'completed': task.completed,
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        task.save()
        return JsonResponse({'message': 'Task updated successfully', 'task': {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'created_at': task.created_at.isoformat(),
            'completed': task.completed,
        }})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully.'}, status=204)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)