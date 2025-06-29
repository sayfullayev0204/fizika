from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Assignment, Submission, Grade, Subject, StudentGroup, Curriculum, Test, Question

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        label="Ism",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingizni kiriting'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        label="Familiya",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangizni kiriting'})
    )
    email = forms.EmailField(
        required=True, 
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi nomini kiriting'})
    )
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni kiriting'})
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni takrorlang'})
    )
    student_group = forms.ModelChoiceField(
        queryset=StudentGroup.objects.all(),
        required=False,
        empty_label="Guruhni tanlang",
        label="Guruh",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'student_group_select'})
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "student_group", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Fan nomini kiriting'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Fan haqida qisqacha ma\'lumot'
            }),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'subject', 'groups', 'file', 'deadline', 'max_score']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Topshiriq nomini kiriting'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Topshiriq tavsifini kiriting'
            }),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'groups': forms.CheckboxSelectMultiple(),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
            'max_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 100,
                'value': 50,
                'placeholder': 'Maksimal ball (1-100)'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(teacher=user)
            self.fields['groups'].queryset = StudentGroup.objects.filter(subject__teacher=user)

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file', 'comment']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Qo\'shimcha izoh (ixtiyoriy)'
            }),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score', 'comment']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Ball kiriting (0-50)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Baho haqida izoh'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.submission = kwargs.pop('submission', None)
        super().__init__(*args, **kwargs)
        if self.submission:
            max_score = self.submission.assignment.max_score
            self.fields['score'].widget.attrs.update({
                'max': max_score,
                'placeholder': f'Ball kiriting (0-{max_score})'
            })
            self.fields['score'].help_text = f'Maksimal ball: {max_score}'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk and self.submission:  # New instance, set submission
            instance.submission = self.submission
        if commit:
            instance.save()
        return instance
    
class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ['title', 'description', 'subject', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'O\'quv reja nomini kiriting'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'O\'quv reja haqida ma\'lumot'
            }),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={
                'class': 'form-control', 
                'accept': '.pdf,.doc,.docx'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(teacher=user)
            self.fields['subject'].empty_label = "Umumiy o'quv reja"

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'subject', 'time_limit', 'max_score']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Test nomini kiriting'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Test haqida ma\'lumot'
            }),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'time_limit': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 5, 
                'max': 180, 
                'value': 30
            }),
            'max_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 10,
                'max': 100,
                'value': 50,
                'placeholder': 'Maksimal ball (10-100)'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(teacher=user)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'points']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Savol matnini kiriting'
            }),
            'option_a': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'A variant'
            }),
            'option_b': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'B variant'
            }),
            'option_c': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'C variant'
            }),
            'option_d': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'D variant'
            }),
            'correct_answer': forms.Select(attrs={'class': 'form-select'}),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'value': 1,
                'placeholder': 'Ball qiymati (1-10)'
            }),
        }
