from django.db import models


# Users
class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # user_id
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Categories
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)  # category_id
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# Courses
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)  # course_id
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title


# Enrollments
class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)  # enrollment_id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('enrolled', 'Enrolled'), ('completed', 'Completed')])

    class Meta:
        unique_together = ['user', 'course', 'status']

    def __str__(self):
        return f'{self.user.username} - {self.course.title} - {self.status}'


# Lessons
class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)  # lesson_id
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField()

    def __str__(self):
        return self.title


# Reviews
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)  # review_id
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'


# Payments
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)  # Ensure this field is included
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    class Meta:
        unique_together = ['user', 'course', 'status']

    def __str__(self):
        return f'{self.user.username} - {self.course.title} - {self.amount}'



# Quizzes
class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)  # quiz_id
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    total_marks = models.IntegerField()

    def __str__(self):
        return self.title


# QuizQuestions
class QuizQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)  # question_id
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])

    def __str__(self):
        return f'{self.quiz.title} - {self.question_text}'


# UserProgress
class UserProgress(models.Model):
    progress_id = models.AutoField(primary_key=True)  # progress_id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.IntegerField()
    quiz_scores = models.JSONField()  # Store quiz scores as a JSON object

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'
