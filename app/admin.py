from django.contrib import admin
from .models import Subject, StudentGroup, Assignment, Submission, Grade, Curriculum, Test, Question, TestResult

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'created_at']
    list_filter = ['teacher', 'created_at']
    search_fields = ['name', 'teacher__username', 'teacher__first_name', 'teacher__last_name']
    ordering = ['name']

@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'student_count']
    list_filter = ['subject']
    search_fields = ['name', 'subject__name']
    filter_horizontal = ['students']
    
    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'O\'quvchilar soni'

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'teacher', 'deadline', 'is_expired', 'created_at']
    list_filter = ['subject', 'teacher', 'deadline', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['groups']
    date_hierarchy = 'deadline'
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Muddati tugagan'

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'has_grade']
    list_filter = ['assignment__subject', 'submitted_at']
    search_fields = ['assignment__title', 'student__username', 'student__first_name', 'student__last_name']
    
    def has_grade(self, obj):
        return hasattr(obj, 'score')
    has_grade.boolean = True
    has_grade.short_description = 'Baholangan'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['submission', 'score', 'graded_at']
    list_filter = ['score', 'graded_at']
    search_fields = ['submission__student__username', 'submission__assignment__title']

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created_by', 'created_at']
    list_filter = ['subject', 'created_by', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'time_limit', 'question_count', 'is_active', 'created_by', 'created_at']
    list_filter = ['subject', 'is_active', 'created_by', 'created_at']
    search_fields = ['title', 'description']
    
    def question_count(self, obj):
        return obj.question_set.count()
    question_count.short_description = 'Savollar soni'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'question_text_short', 'correct_answer']
    list_filter = ['test', 'correct_answer']
    search_fields = ['question_text', 'test__title']
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Savol matni'

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['test', 'student', 'score', 'correct_answers', 'total_questions', 'percentage', 'completed_at']
    list_filter = ['test', 'completed_at']
    search_fields = ['test__title', 'student__username', 'student__first_name', 'student__last_name']
    readonly_fields = ['score', 'correct_answers', 'total_questions', 'completed_at']
    
    def percentage(self, obj):
        return f"{obj.get_percentage()}%"
    percentage.short_description = 'Foiz'
