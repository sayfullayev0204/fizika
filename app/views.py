from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from .models import Subject, Assignment, Submission, Grade, StudentGroup, Curriculum, Test, Question, TestResult
from .forms import AssignmentForm, SubmissionForm, GradeForm, CustomUserCreationForm, SubjectForm, CurriculumForm, TestForm, QuestionForm
import json

def home(request):
    if request.user.is_authenticated:
        # Check if user is teacher or admin
        if request.user.groups.filter(name='Teachers').exists() or request.user.is_superuser:
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')
    
    # Agar user login qilmagan bo'lsa - sayt haqida ma'lumot
    context = {
        'total_subjects': Subject.objects.count(),
        'total_teachers': User.objects.filter(groups__name='Teachers').count(),
        'total_students': User.objects.filter(groups__name='Students').count(),
        'total_assignments': Assignment.objects.count(),
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def author(request):
    return render(request, 'author.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        user_type = request.POST.get('user_type', 'student')
        
        if form.is_valid():
            user = form.save()
            student_group = form.cleaned_data.get('student_group')
            
            # Add user to appropriate group
            if user_type == 'admin':
                # Admin uchun superuser qilamiz
                user.is_staff = True
                user.is_superuser = True
                user.save()
                # Teachers guruhiga ham qo'shamiz
                teacher_group, created = Group.objects.get_or_create(name='Teachers')
                user.groups.add(teacher_group)
            elif user_type == 'teacher':
                teacher_group, created = Group.objects.get_or_create(name='Teachers')
                user.groups.add(teacher_group)
            else:
                student_group_obj, created = Group.objects.get_or_create(name='Students')
                user.groups.add(student_group_obj)
                
                # Agar guruh tanlangan bo'lsa, o'quvchini shu guruhga qo'shamiz
                if student_group:
                    student_group.students.add(user)
            
            username = form.cleaned_data.get('username')
            if user_type == 'admin':
                user_type_text = 'Administrator'
            elif user_type == 'teacher':
                user_type_text = 'O\'qituvchi'
            else:
                user_type_text = 'O\'quvchi'
                
            messages.success(request, f'{username} uchun {user_type_text} hisobi yaratildi!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
        'student_groups': StudentGroup.objects.all()
    }
    return render(request, 'registration/register.html', context)

@login_required
def teacher_dashboard(request):
    # Check if user is teacher or admin
    if not (request.user.groups.filter(name='Teachers').exists() or request.user.is_superuser):
        messages.error(request, 'Sizga bu sahifaga kirish ruxsati yo\'q!')
        return redirect('student_dashboard')
    
    subjects = Subject.objects.filter(teacher=request.user)
    recent_assignments = Assignment.objects.filter(teacher=request.user)[:5]
    
    # Statistics
    total_students = User.objects.filter(
        studentgroup__subject__teacher=request.user
    ).distinct().count()
    
    total_submissions = Submission.objects.filter(
        assignment__teacher=request.user
    ).count()
    
    context = {
        'subjects': subjects,
        'recent_assignments': recent_assignments,
        'total_students': total_students,
        'total_submissions': total_submissions,
    }
    return render(request, 'teacher/dashboard.html', context)

@login_required
def student_dashboard(request):
    # O'quvchi a'zo bo'lgan guruhlar orqali fanlarni olish
    groups = StudentGroup.objects.filter(students=request.user)
    subjects = Subject.objects.filter(studentgroup__in=groups).distinct()
    
    # Yaqinda qo'shilgan topshiriqlar
    recent_assignments = Assignment.objects.filter(
        groups__students=request.user
    ).distinct()[:5]
    
    context = {
        'subjects': subjects,
        'recent_assignments': recent_assignments,
    }
    return render(request, 'student/dashboard.html', context)

@login_required
def create_assignment(request):
    if not (request.user.groups.filter(name='Teachers').exists() or request.user.is_superuser):
        messages.error(request, 'Sizga bu sahifaga kirish ruxsati yo\'q!')
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            form.save_m2m()  # ManyToMany maydonlarni saqlash
            messages.success(request, 'Topshiriq muvaffaqiyatli yaratildi!')
            return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Formada xatoliklar mavjud!')
    else:
        form = AssignmentForm(user=request.user)
    
    return render(request, 'teacher/create_assignment.html', {'form': form})

@login_required
def create_subject(request):
    if not (request.user.groups.filter(name='Teachers').exists() or request.user.is_superuser):
        messages.error(request, 'Sizga bu sahifaga kirish ruxsati yo\'q!')
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.teacher = request.user
            subject.save()
            messages.success(request, 'Fan muvaffaqiyatli yaratildi!')
            return redirect('teacher_dashboard')
    else:
        form = SubjectForm()
    
    return render(request, 'teacher/create_subject.html', {'form': form})

# O'quv reja views
@login_required
def curriculum_list(request):
    curriculums = Curriculum.objects.all().order_by('-created_at')
    subjects = Subject.objects.all()
    
    # Filter by subject if provided
    subject_id = request.GET.get('subject')
    if subject_id:
        curriculums = curriculums.filter(subject_id=subject_id)
    
    context = {
        'curriculums': curriculums,
        'subjects': subjects,
        'selected_subject': int(subject_id) if subject_id else None,
    }
    return render(request, 'curriculum/list.html', context)

@login_required
def create_curriculum(request):
    if not (request.user.groups.filter(name='Teachers').exists() or request.user.is_superuser):
        messages.error(request, 'Sizga bu sahifaga kirish ruxsati yo\'q!')
        return redirect('curriculum_list')
    
    if request.method == 'POST':
        form = CurriculumForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            curriculum = form.save(commit=False)
            curriculum.created_by = request.user
            curriculum.save()
            messages.success(request, 'O\'quv reja muvaffaqiyatli yaratildi!')
            return redirect('curriculum_list')
    else:
        form = CurriculumForm(user=request.user)
    
    return render(request, 'curriculum/create.html', {'form': form})

# Test views
@login_required
def test_list(request):
    subjects = Subject.objects.all()
    tests = Test.objects.filter(is_active=True)
    
    # Filter by subject if provided
    subject_id = request.GET.get('subject')
    if subject_id:
        tests = tests.filter(subject_id=subject_id)
    
    context = {
        'tests': tests,
        'subjects': subjects,
        'selected_subject': int(subject_id) if subject_id else None,
    }
    return render(request, 'tests/list.html', context)

@login_required
def create_test(request):
    if not (request.user.groups.filter(name='Teachers').exists() or request.user.is_superuser):
        messages.error(request, 'Sizga bu sahifaga kirish ruxsati yo\'q!')
        return redirect('test_list')
    
    if request.method == 'POST':
        form = TestForm(request.POST, user=request.user)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()
            messages.success(request, 'Test muvaffaqiyatli yaratildi!')
            return redirect('test_detail', test_id=test.id)
        else:
            messages.error(request, 'Formada xatoliklar mavjud!')
    else:
        form = TestForm(user=request.user)
    
    return render(request, 'tests/create.html', {'form': form})

@login_required
def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = Question.objects.filter(test=test)
    
    # Check if user already took this test
    user_result = None
    if not (request.user.groups.filter(name='Teachers').exists() or request.user.is_superuser):
        try:
            user_result = TestResult.objects.get(test=test, student=request.user)
        except TestResult.DoesNotExist:
            pass
    
    context = {
        'test': test,
        'questions': questions,
        'user_result': user_result,
        'is_teacher': request.user.groups.filter(name='Teachers').exists() or request.user.is_superuser,
    }
    return render(request, 'tests/detail.html', context)

@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    
    # Check if user already took this test
    if TestResult.objects.filter(test=test, student=request.user).exists():
        messages.warning(request, 'Siz bu testni allaqachon topshirgansiz!')
        return redirect('test_detail', test_id=test_id)
    
    questions = Question.objects.filter(test=test)
    
    if request.method == 'POST':
        correct_answers = 0
        total_questions = questions.count()
        total_score = 0
        
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer == question.correct_answer:
                correct_answers += 1
                total_score += question.points
        
        # Save result
        TestResult.objects.create(
            test=test,
            student=request.user,
            score=total_score,
            total_questions=total_questions,
            correct_answers=correct_answers
        )
        
        percentage = round((total_score / test.max_score) * 100, 1)
        messages.success(request, f'Test yakunlandi! Natijangiz: {total_score}/{test.max_score} ball ({percentage}%)')
        return redirect('test_detail', test_id=test_id)
    
    context = {
        'test': test,
        'questions': questions,
    }
    return render(request, 'tests/take.html', context)

@login_required
def add_question(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    
    if test.created_by != request.user and not request.user.is_superuser:
        messages.error(request, 'Sizga bu testga savol qo\'shish ruxsati yo\'q!')
        return redirect('test_detail', test_id=test_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            messages.success(request, 'Savol muvaffaqiyatli qo\'shildi!')
            return redirect('test_detail', test_id=test_id)
    else:
        form = QuestionForm()
    
    context = {
        'form': form,
        'test': test,
    }
    return render(request, 'tests/add_question.html', context)

@login_required
def assignment_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    # O'qituvchi uchun
    if subject.teacher == request.user or request.user.is_superuser:
        assignments = Assignment.objects.filter(subject=subject)
        template = 'teacher/assignment_list.html'
    else:
        # O'quvchi uchun - faqat o'zi a'zo bo'lgan guruhlardagi topshiriqlar
        user_groups = StudentGroup.objects.filter(students=request.user, subject=subject)
        assignments = Assignment.objects.filter(
            subject=subject,
            groups__in=user_groups
        ).distinct()
        template = 'student/assignment_list.html'
    
    context = {
        'subject': subject,
        'assignments': assignments,
    }
    return render(request, template, context)

@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # O'qituvchi uchun
    if assignment.teacher == request.user or request.user.is_superuser:
        submissions = Submission.objects.filter(assignment=assignment)
        context = {
            'assignment': assignment,
            'submissions': submissions,
        }
        return render(request, 'teacher/assignment_detail.html', context)
    
    # O'quvchi uchun
    else:
        # O'quvchi bu topshiriqqa kirish huquqi bormi tekshirish
        user_groups = StudentGroup.objects.filter(students=request.user)
        if not assignment.groups.filter(id__in=user_groups).exists():
            raise Http404("Bu topshiriqqa kirishga ruxsatingiz yo'q")
        
        try:
            submission = Submission.objects.get(assignment=assignment, student=request.user)
        except Submission.DoesNotExist:
            submission = None
        
        context = {
            'assignment': assignment,
            'submission': submission,
            'is_expired': assignment.is_expired(),
        }
        return render(request, 'student/assignment_detail.html', context)

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Muddat tugaganmi tekshirish
    if assignment.is_expired():
        messages.error(request, 'Topshiriq muddati tugagan!')
        return redirect('assignment_detail', assignment_id=assignment_id)
    
    # O'quvchi bu topshiriqqa kirish huquqi bormi tekshirish
    user_groups = StudentGroup.objects.filter(students=request.user)
    if not assignment.groups.filter(id__in=user_groups).exists():
        raise Http404("Bu topshiriqqa kirishga ruxsatingiz yo'q")
    
    try:
        submission = Submission.objects.get(assignment=assignment, student=request.user)
    except Submission.DoesNotExist:
        submission = None
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Topshiriq muvaffaqiyatli yuborildi!')
            return redirect('assignment_detail', assignment_id=assignment_id)
    else:
        form = SubmissionForm(instance=submission)
    
    context = {
        'assignment': assignment,
        'form': form,
        'submission': submission,
    }
    return render(request, 'student/submit_assignment.html', context)


@login_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Faqat o'qituvchi baho qo'ya oladi
    if submission.assignment.teacher != request.user and not request.user.is_superuser:
        raise Http404("Sizga bu amalni bajarishga ruxsat yo'q")
    
    try:
        grade = Grade.objects.get(submission=submission)
    except Grade.DoesNotExist:
        grade = None
    
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade, submission=submission)
        if form.is_valid():
            grade = form.save(commit=False)  # Save without committing to DB
            if not grade.submission:  # Ensure submission is set for new grades
                grade.submission = submission
            grade.save()
            messages.success(request, 'Ball muvaffaqiyatli qo\'yildi!')
            return redirect('assignment_detail', assignment_id=submission.assignment.id)
        else:
            messages.error(request, 'Formada xatoliklar mavjud!')
    else:
        form = GradeForm(instance=grade, submission=submission)
    
    context = {
        'submission': submission,
        'form': form,
        'grade': grade,
    }
    return render(request, 'teacher/grade_submission.html', context)
@login_required
def student_grades(request):
    submissions = Submission.objects.filter(student=request.user)
    grades = Grade.objects.filter(submission__in=submissions).order_by('-graded_at')
    
    context = {
        'grades': grades,
    }
    return render(request, 'student/grades.html', context)
