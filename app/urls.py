from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Asosiy sahifalar
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('author/', views.author, name='author'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    
    # Fanlar
    path('create-subject/', views.create_subject, name='create_subject'),
    
    # Topshiriqlar
    path('create-assignment/', views.create_assignment, name='create_assignment'),
    path('subject/<int:subject_id>/assignments/', views.assignment_list, name='assignment_list'),
    path('subject/<int:subject_id>/assignments/<str:assignment_type>/', views.assignment_list_by_type, name='assignment_list_by_type'),
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
    
    # Hujjatlar
    path('documents/', views.document_list, name='document_list'),
    path('documents/<str:document_type>/', views.document_list_by_type, name='document_list_by_type'),
    path('documents/create/', views.create_document, name='create_document'),
    path('documents/<int:document_id>/', views.document_detail, name='document_detail'),

    path('videos/', views.videos, name='videos'),
    path('video/create/', views.create_video, name='create_video'),
    path('video/<int:id>/', views.video_detail, name='video_detail'),
    path('video/<int:id>/edit/', views.edit_video, name='edit_video'),
]
