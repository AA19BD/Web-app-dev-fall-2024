from rest_framework import serializers
from .models import User, Category, Course, Enrollment, Lesson, Review, Payment, Quiz, QuizQuestion, UserProgress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'is_student', 'is_instructor']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name', 'description']


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['course_id', 'title', 'description', 'price', 'category', 'created_at', 'instructor']


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['enrollment_id', 'user', 'course', 'enrollment_date', 'status']


class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = ['lesson_id', 'course', 'title', 'content', 'video_url']


class ReviewSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['review_id', 'course', 'user', 'rating', 'comment', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['payment_id', 'user', 'amount', 'payment_date', 'status']


class QuizSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = ['quiz_id', 'course', 'title', 'total_marks']


class QuizQuestionSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ['question_id', 'quiz', 'question_text', 'option_a',
                  'option_b', 'option_c', 'option_d', 'correct_option']


class UserProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = UserProgress
        fields = ['progress_id', 'user', 'course', 'completed_lessons', 'quiz_scores']
