from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import redirect

def log_out(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

urlpatterns = [
    # Asosiy sahifalar
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('author/', views.author, name='author'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', log_out, name='logout'),
    
    # Dashboard
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    
    # Fanlar
    path('create-subject/', views.create_subject, name='create_subject'),
    
    # Topshiriqlar
    path('create-assignment/', views.create_assignment, name='create_assignment'),
    path('subject/<int:subject_id>/assignments/', views.assignment_list, name='assignment_list'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    
    # Baholar
    path('submission/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
    path('my-grades/', views.student_grades, name='student_grades'),
    
    # O'quv rejalar
    path('curriculum/', views.curriculum_list, name='curriculum_list'),
    path('curriculum/create/', views.create_curriculum, name='create_curriculum'),
    
    # Testlar
    path('tests/', views.test_list, name='test_list'),
    path('tests/create/', views.create_test, name='create_test'),
    path('tests/<int:test_id>/', views.test_detail, name='test_detail'),
    path('tests/<int:test_id>/take/', views.take_test, name='take_test'),
    path('tests/<int:test_id>/add-question/', views.add_question, name='add_question'),
]
