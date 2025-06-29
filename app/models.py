from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Fan nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="O'qituvchi")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
        ordering = ['name']

class StudentGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name="Guruh nomi")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
    students = models.ManyToManyField(User, blank=True, verbose_name="O'quvchilar")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject.name}"
    
    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        ordering = ['name']

def assignment_file_path(instance, filename):
    return f'assignments/{instance.subject.id}/{filename}'

class Assignment(models.Model):
    title = models.CharField(max_length=200, verbose_name="Topshiriq nomi")
    description = models.TextField(verbose_name="Tavsif")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
    groups = models.ManyToManyField(StudentGroup, verbose_name="Guruhlar")
    file = models.FileField(upload_to=assignment_file_path, blank=True, null=True, verbose_name="Fayl")
    deadline = models.DateTimeField(verbose_name="Muddat")
    max_score = models.IntegerField(default=50, verbose_name="Maksimal ball")
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="O'qituvchi")
    
    def is_expired(self):
        return timezone.now() > self.deadline
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Topshiriq"
        verbose_name_plural = "Topshiriqlar"
        ordering = ['-created_at']

def submission_file_path(instance, filename):
    return f'submissions/{instance.assignment.id}/{instance.student.id}/{filename}'

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name="Topshiriq")
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="O'quvchi")
    file = models.FileField(upload_to=submission_file_path, blank=True, null=True, verbose_name="Fayl")
    comment = models.TextField(blank=True, verbose_name="Izoh")
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Topshiriq javob"
        verbose_name_plural = "Topshiriq javoblar"
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']

class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, verbose_name="Topshiriq javob")
    score = models.IntegerField(verbose_name="Ball (0-50)", help_text="0 dan 50 gacha ball kiriting")
    comment = models.TextField(blank=True, verbose_name="O'qituvchi izohi")
    graded_at = models.DateTimeField(auto_now_add=True)
    
    def get_percentage(self):
        max_score = self.submission.assignment.max_score
        return round((self.score / max_score) * 100, 1)
    
    def get_grade_level(self):
        percentage = self.get_percentage()
        if percentage >= 90:
            return "A'lo"
        elif percentage >= 70:
            return "Yaxshi"
        elif percentage >= 50:
            return "Qoniqarli"
        else:
            return "Qoniqarsiz"
    
    def get_grade_class(self):
        percentage = self.get_percentage()
        if percentage >= 90:
            return "excellent"
        elif percentage >= 70:
            return "good"
        elif percentage >= 50:
            return "satisfactory"
        else:
            return "poor"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not hasattr(self, 'submission') or self.submission is None:
            return  # Skip validation if submission is not set
        max_score = self.submission.assignment.max_score
        if self.score < 0 or self.score > max_score:
            raise ValidationError(f'Ball 0 dan {max_score} gacha bo\'lishi kerak')
        def __str__(self):
            return f"{self.submission.student.username} - {self.score}/{self.submission.assignment.max_score}"
        
    class Meta:
        verbose_name = "Baho"
        verbose_name_plural = "Baholar"
        ordering = ['-graded_at']

def curriculum_file_path(instance, filename):
    return f'curriculum/{filename}'

class Curriculum(models.Model):
    title = models.CharField(max_length=200, verbose_name="O'quv reja nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    file = models.FileField(upload_to=curriculum_file_path, verbose_name="Fayl")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yaratuvchi")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "O'quv reja"
        verbose_name_plural = "O'quv rejalar"
        ordering = ['-created_at']

class Test(models.Model):
    title = models.CharField(max_length=200, verbose_name="Test nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
    time_limit = models.IntegerField(default=30, verbose_name="Vaqt chegarasi (daqiqa)")
    max_score = models.IntegerField(default=50, verbose_name="Maksimal ball")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yaratuvchi")
    
    def get_questions_count(self):
        return self.questions.count()
    
    def get_average_score(self):
        results = self.testresult_set.all()
        if results:
            return round(sum(result.score for result in results) / len(results), 1)
        return 0
    
    def __str__(self):
        return f"{self.title} - {self.subject.name}"
    
    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"
        ordering = ['-created_at']

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Test", related_name='questions')
    question_text = models.TextField(verbose_name="Savol matni")
    option_a = models.CharField(max_length=200, verbose_name="A variant")
    option_b = models.CharField(max_length=200, verbose_name="B variant")
    option_c = models.CharField(max_length=200, verbose_name="C variant")
    option_d = models.CharField(max_length=200, verbose_name="D variant")
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'A variant'),
        ('B', 'B variant'),
        ('C', 'C variant'),
        ('D', 'D variant'),
    ], verbose_name="To'g'ri javob")
    points = models.IntegerField(default=1, verbose_name="Ball qiymati")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.test.title} - {self.question_text[:50]}..."
    
    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
        ordering = ['created_at']

class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Test")
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="O'quvchi")
    score = models.IntegerField(verbose_name="Olingan ball")
    total_questions = models.IntegerField(verbose_name="Jami savollar")
    correct_answers = models.IntegerField(verbose_name="To'g'ri javoblar")
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def get_percentage(self):
        return round((self.score / self.test.max_score) * 100, 1)
    
    def get_grade_level(self):
        percentage = self.get_percentage()
        if percentage >= 90:
            return "A'lo"
        elif percentage >= 70:
            return "Yaxshi"
        elif percentage >= 50:
            return "Qoniqarli"
        else:
            return "Qoniqarsiz"
    
    def get_grade_class(self):
        percentage = self.get_percentage()
        if percentage >= 90:
            return "excellent"
        elif percentage >= 70:
            return "good"
        elif percentage >= 50:
            return "satisfactory"
        else:
            return "poor"
    
    def __str__(self):
        return f"{self.student.username} - {self.test.title} - {self.score}/{self.test.max_score}"
    
    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"
        ordering = ['-completed_at']
        unique_together = ['test', 'student']
