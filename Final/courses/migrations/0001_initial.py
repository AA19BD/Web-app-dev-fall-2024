# Generated by Django 4.2 on 2024-12-22 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.category')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('total_marks', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('is_student', models.BooleanField(default=True)),
                ('is_instructor', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('progress_id', models.AutoField(primary_key=True, serialize=False)),
                ('completed_lessons', models.IntegerField()),
                ('quiz_scores', models.JSONField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.user')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.user')),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
                ('option_a', models.CharField(max_length=255)),
                ('option_b', models.CharField(max_length=255)),
                ('option_c', models.CharField(max_length=255)),
                ('option_d', models.CharField(max_length=255)),
                ('correct_option', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], max_length=1)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.user')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('lesson_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('video_url', models.URLField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('enrollment_id', models.AutoField(primary_key=True, serialize=False)),
                ('enrollment_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('enrolled', 'Enrolled'), ('completed', 'Completed')], max_length=50)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.user')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.user'),
        ),
    ]