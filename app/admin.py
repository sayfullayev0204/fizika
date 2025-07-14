from django.contrib import admin
from .models import (
    Subject, StudentGroup, Assignment, Submission, Grade,
    Curriculum, Test, Question, TestResult, Document, Video
)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'created_at')
    list_filter = ('teacher', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'teacher')
        }),
    )

@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'get_student_count', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('name', 'subject__name')
    filter_horizontal = ('students',)
    date_hierarchy = 'created_at'
    ordering = ('name',)

    def get_student_count(self, obj):
        return obj.students.count()
    get_student_count.short_description = "O'quvchilar soni"

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'assignment_type', 'deadline', 'is_expired', 'max_score', 'teacher')
    list_filter = ('assignment_type', 'subject', 'deadline', 'teacher')
    search_fields = ('title', 'description', 'subject__name')
    filter_horizontal = ('groups',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'assignment_type', 'subject', 'groups', 'file', 'deadline', 'max_score', 'teacher')
        }),
    )

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at')
    list_filter = ('assignment__subject', 'submitted_at')
    search_fields = ('assignment__title', 'student__username', 'comment')
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)
    fieldsets = (
        (None, {
            'fields': ('assignment', 'student', 'file', 'comment')
        }),
    )

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('submission', 'score', 'get_percentage', 'get_grade_level', 'graded_at')
    list_filter = ('submission__assignment__subject', 'graded_at')
    search_fields = ('submission__assignment__title', 'submission__student__username', 'comment')
    date_hierarchy = 'graded_at'
    ordering = ('-graded_at',)
    fieldsets = (
        (None, {
            'fields': ('submission', 'score', 'comment')
        }),
    )

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_by', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title', 'description', 'subject__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'file', 'subject', 'created_by')
        }),
    )

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'time_limit', 'max_score', 'is_active', 'get_questions_count', 'get_average_score')
    list_filter = ('subject', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'subject__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'subject', 'time_limit', 'max_score', 'is_active', 'created_by')
        }),
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'question_text', 'correct_answer', 'points', 'created_at')
    list_filter = ('test__subject', 'created_at')
    search_fields = ('question_text', 'test__title')
    date_hierarchy = 'created_at'
    ordering = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('test', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'points')
        }),
    )

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test', 'student', 'score', 'get_percentage', 'get_grade_level', 'completed_at')
    list_filter = ('test__subject', 'completed_at')
    search_fields = ('test__title', 'student__username')
    date_hierarchy = 'completed_at'
    ordering = ('-completed_at',)
    fieldsets = (
        (None, {
            'fields': ('test', 'student', 'score', 'total_questions', 'correct_answers')
        }),
    )

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'subject', 'created_by', 'created_at')
    list_filter = ('document_type', 'subject', 'created_at')
    search_fields = ('title', 'subject__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'document_type', 'file', 'subject', 'created_by')
        }),
    )

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_by', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title', 'description', 'subject__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'file', 'subject', 'created_by')
        }),
    )