from django.urls import path
from .views import task_list, task_detail, task_create, task_update, task_delete

urlpatterns = [
    path('', task_list, name='task_list'),
    path('task/<int:task_id>/', task_detail, name='task_detail'),
    path('task/add/', task_create, name='task_create'),
    path('task/<int:task_id>/edit/', task_update, name='task_update'),
    path('task/<int:task_id>/delete/', task_delete, name='task_delete'),
]