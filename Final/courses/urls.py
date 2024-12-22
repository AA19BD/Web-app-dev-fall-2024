from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CategoryViewSet, CourseViewSet, EnrollmentViewSet, LessonViewSet, ReviewViewSet, PaymentViewSet, QuizViewSet, QuizQuestionViewSet, UserProgressViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'quizquestions', QuizQuestionViewSet)
router.register(r'userprogress', UserProgressViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]