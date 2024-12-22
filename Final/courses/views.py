from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User, Category, Course, Enrollment, Lesson, Review, Payment, Quiz, QuizQuestion, UserProgress, \
    UserQuizAnswer
from .serializers import UserSerializer, CategorySerializer, CourseSerializer, EnrollmentSerializer, LessonSerializer, \
    ReviewSerializer, PaymentSerializer, QuizSerializer, QuizQuestionSerializer, UserProgressSerializer, \
    UserQuizAnswerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # def create(self, request, *args, **kwargs):
    #     # Automatically assign the user to the payment
    #     data = request.data.copy()
    #     data['user'] = request.user.id  # Ensure the logged-in user is set for payment
    #     serializer = self.get_serializer(data=data)
    #
    #     if serializer.is_valid():
    #         serializer.save()  # Save the payment with the assigned user
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizQuestionViewSet(viewsets.ModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer


class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        data['user'] = request.user.id

        course_id = request.data.get('course')
        if not course_id:
            return Response({"detail": "Course is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()  # Save the UserProgress instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizSubmissionViewSet(viewsets.ModelViewSet):
    queryset = UserQuizAnswer.objects.all()
    serializer_class = UserQuizAnswerSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        data['user'] = request.user.id

        quiz_id = data.get('quiz')
        question_id = data.get('question')
        selected_option = data.get('selected_option')

        if not quiz_id or not question_id or not selected_option:
            return Response({"detail": "Quiz, question, and selected_option are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quiz = Quiz.objects.get(quiz_id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            question = QuizQuestion.objects.get(question_id=question_id)
        except QuizQuestion.DoesNotExist:
            return Response({"detail": "Question not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save(quiz=quiz, question=question, selected_option=selected_option)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class QuizSubmissionViewSet(viewsets.ModelViewSet):
#     queryset = UserQuizAnswer.objects.all()
#     serializer_class = UserQuizAnswerSerializer
#
#     def create(self, request, *args, **kwargs):
#         # Make a copy of the request data to modify it
#         data = request.data.copy()
#
#         # Automatically assign the user from the request
#         data['user'] = request.user.id  # Automatically set the logged-in user
#
#         # Ensure that the quiz and question IDs are present
#         quiz_id = data.get('quiz')
#         question_id = data.get('question')
#         selected_option = data.get('selected_option')
#
#         if not quiz_id or not question_id or not selected_option:
#             return Response({"detail": "Quiz, question, and selected_option are required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Ensure the quiz exists
#         try:
#             quiz = Quiz.objects.get(quiz_id=quiz_id)
#         except Quiz.DoesNotExist:
#             return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)
#
#         # Ensure the question exists
#         try:
#             question = QuizQuestion.objects.get(question_id=question_id)
#         except QuizQuestion.DoesNotExist:
#             return Response({"detail": "Question not found."}, status=status.HTTP_404_NOT_FOUND)
#
#         # Proceed to create the UserQuizAnswer instance
#         serializer = self.get_serializer(data=data)
#
#         if serializer.is_valid():
#             # Save the UserQuizAnswer instance
#             user_quiz_answer = serializer.save(quiz=quiz, question=question, selected_option=selected_option)
#
#             # Calculate the score (1 point per correct answer)
#             correct_answers = 0
#             if selected_option == question.correct_option:
#                 correct_answers += 1
#
#             # Calculate the total score for the quiz (could be percentage based or absolute score)
#             total_questions = quiz.quizquestion_set.count()  # Total number of questions in the quiz
#             score = (correct_answers / total_questions) * 100 if total_questions else 0
#
#             # Track the user's progress
#             user_progress, created = UserProgress.objects.update_or_create(
#                 user=request.user,
#                 course=quiz.course,
#                 defaults={
#                     'quiz_scores': score,
#                     'completed_lessons': 1  # Increment the completed lessons count (you can modify this logic)
#                 }
#             )
#
#             return Response({
#                 "score": score,
#                 "completed_lessons": user_progress.completed_lessons,
#                 "detail": "Quiz submitted successfully."
#             }, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


