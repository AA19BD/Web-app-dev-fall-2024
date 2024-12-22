from django.contrib import admin
from .models import User, Category, Course, Enrollment, Lesson, Review, Payment, Quiz, QuizQuestion, UserProgress


# User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_student', 'is_instructor')
    search_fields = ('username', 'email')
    list_filter = ('is_student', 'is_instructor')
    ordering = ('username',)


admin.site.register(User, UserAdmin)


# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


# Course Admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'price', 'created_at')
    search_fields = ('title', 'instructor__username', 'category__name')
    list_filter = ('category', 'instructor')
    ordering = ('created_at',)


admin.site.register(Course, CourseAdmin)


# Enrollment Admin
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'enrollment_date')
    search_fields = ('user__username', 'course__title')
    list_filter = ('status',)
    ordering = ('enrollment_date',)


admin.site.register(Enrollment, EnrollmentAdmin)


# Lesson Admin
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'video_url')
    search_fields = ('course__title', 'title')
    list_filter = ('course',)


admin.site.register(Lesson, LessonAdmin)


# Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    search_fields = ('course__title', 'user__username')
    list_filter = ('rating',)
    ordering = ('created_at',)


admin.site.register(Review, ReviewAdmin)


# Payment Admin
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_date', 'status')
    search_fields = ('user__username',)
    list_filter = ('status',)
    ordering = ('payment_date',)


admin.site.register(Payment, PaymentAdmin)


# Quiz Admin
class QuizAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'total_marks')
    search_fields = ('course__title', 'title')
    list_filter = ('course',)


admin.site.register(Quiz, QuizAdmin)


# Quiz Question Admin
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text', 'correct_option')
    search_fields = ('quiz__title', 'question_text')
    list_filter = ('quiz',)


admin.site.register(QuizQuestion, QuizQuestionAdmin)


# User Progress Admin
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'completed_lessons')
    search_fields = ('user__username', 'course__title')
    list_filter = ('course',)


admin.site.register(UserProgress, UserProgressAdmin)
