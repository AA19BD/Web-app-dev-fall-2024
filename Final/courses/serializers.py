from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Category, Course, Enrollment, Lesson, Review, Payment, Quiz, QuizQuestion, UserProgress, \
    UserQuizAnswer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'is_student', 'is_instructor']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name', 'description']


class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_instructor=True), required=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Course
        fields = ['course_id', 'title', 'description', 'price', 'category', 'created_at', 'instructor']

    @staticmethod
    def validate_category(value):
        # Ensure category exists and is valid
        if not value:
            raise serializers.ValidationError("Category is required.")
        return value

    @staticmethod
    def validate_instructor(value):
        # Ensure the user is actually an instructor
        if not value.is_instructor:
            raise serializers.ValidationError("The user must be an instructor.")
        return value


class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)

    class Meta:
        model = Enrollment
        fields = ['enrollment_id', 'user', 'course', 'enrollment_date', 'status']

    def validate(self, data):
        user = data.get('user')
        course = data.get('course')
        status = data.get('status')

        # Check if the user is already enrolled in the course and status is not 'completed'
        if Enrollment.objects.filter(user=user, course=course, status=status).exists():
            raise serializers.ValidationError("The user is already enrolled in this course.")

        return data


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)

    class Meta:
        model = Lesson
        fields = ['lesson_id', 'course', 'title', 'content', 'video_url']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Review
        fields = ['review_id', 'course', 'user', 'rating', 'comment', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)

    class Meta:
        model = Payment
        fields = ['payment_id', 'user', 'course', 'amount', 'payment_date', 'status']

    def validate(self, data):
        user = data.get('user')
        course = data.get('course')
        status = data.get('status')

        # Check if the user has already made a payment for the course
        if Payment.objects.filter(user=user, course=course, status=status).exists():
            raise serializers.ValidationError("You have already made a payment for this course.")

        return data


class QuizSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)

    class Meta:
        model = Quiz
        fields = ['quiz_id', 'course', 'title', 'total_marks']


class QuizQuestionSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all(), required=True)

    class Meta:
        model = QuizQuestion
        fields = ['question_id', 'quiz', 'question_text', 'option_a',
                  'option_b', 'option_c', 'option_d', 'correct_option']


class UserProgressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)

    class Meta:
        model = UserProgress
        fields = ['progress_id', 'user', 'course', 'completed_lessons', 'quiz_scores']

    # def validate(self, data):
    #     user = data.get('user')
    #     course = data.get('course')
    #
    #     # Validate that the user is not already enrolled or making progress in the same course
    #     if UserProgress.objects.filter(user=user, course=course).exists():
    #         raise serializers.ValidationError("User is already enrolled in this course.")
    #
    #     return data


class UserQuizAnswerSerializer(serializers.ModelSerializer):
    # Ensure quiz and user are included correctly
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Link to the User model
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())  # Link to the Quiz model
    question = serializers.PrimaryKeyRelatedField(queryset=QuizQuestion.objects.all())  # Link to the QuizQuestion model

    selected_option = serializers.ChoiceField(
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')]
    )

    # Including all options from the related QuizQuestion
    option_a = serializers.CharField(source='question.option_a', read_only=True)
    option_b = serializers.CharField(source='question.option_b', read_only=True)
    option_c = serializers.CharField(source='question.option_c', read_only=True)
    option_d = serializers.CharField(source='question.option_d', read_only=True)

    class Meta:
        model = UserQuizAnswer
        fields = ['user', 'quiz', 'question', 'selected_option', 'option_a', 'option_b', 'option_c', 'option_d']

    def validate(self, data):
        user = data.get('user')
        quiz = data.get('quiz')
        question = data.get('question')

        # Check if the user has already answered this question for the quiz
        if UserQuizAnswer.objects.filter(user=user, quiz=quiz, question=question).exists():
            raise serializers.ValidationError("You have already answered this question.")

        return data

    def create(self, validated_data):
        user_quiz_answer = UserQuizAnswer.objects.create(**validated_data)
        return user_quiz_answer