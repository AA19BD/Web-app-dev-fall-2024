from django.db import migrations


def create_default_tasks(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    tasks = [
        {"title": "Learn Django", "description": "Complete the Django tutorial and build a simple project."},
        {"title": "Read Documentation",
         "description": "Read the Django official documentation to understand the framework better."},
        {"title": "Build a Task Manager",
         "description": "Create a simple task management application to practice Django skills."},
        {"title": "Explore Django REST Framework",
         "description": "Start learning about building APIs with Django REST framework."},
        {"title": "Deploy to Heroku", "description": "Deploy the task manager app to Heroku for public access."},
    ]

    for task in tasks:
        Task.objects.create(**task)


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0001_initial'),  # Replace with your last migration file
    ]

    operations = [
        migrations.RunPython(create_default_tasks),
    ]