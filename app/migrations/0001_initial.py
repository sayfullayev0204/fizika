# Generated by Django 5.2.3 on 2025-06-23 15:17

import app.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Fan nomi')),
                ('description', models.TextField(blank=True, verbose_name='Tavsif')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="O'qituvchi")),
            ],
            options={
                'verbose_name': 'Fan',
                'verbose_name_plural': 'Fanlar',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Guruh nomi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('students', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name="O'quvchilar")),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subject', verbose_name='Fan')),
            ],
            options={
                'verbose_name': 'Guruh',
                'verbose_name_plural': 'Guruhlar',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name="O'quv reja nomi")),
                ('description', models.TextField(blank=True, verbose_name='Tavsif')),
                ('file', models.FileField(upload_to=app.models.curriculum_file_path, verbose_name='Fayl')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Yaratuvchi')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.subject', verbose_name='Fan')),
            ],
            options={
                'verbose_name': "O'quv reja",
                'verbose_name_plural': "O'quv rejalar",
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Topshiriq nomi')),
                ('description', models.TextField(verbose_name='Tavsif')),
                ('file', models.FileField(blank=True, null=True, upload_to=app.models.assignment_file_path, verbose_name='Fayl')),
                ('deadline', models.DateTimeField(verbose_name='Muddat')),
                ('max_score', models.IntegerField(default=50, verbose_name='Maksimal ball')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="O'qituvchi")),
                ('groups', models.ManyToManyField(to='app.studentgroup', verbose_name='Guruhlar')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subject', verbose_name='Fan')),
            ],
            options={
                'verbose_name': 'Topshiriq',
                'verbose_name_plural': 'Topshiriqlar',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=app.models.submission_file_path, verbose_name='Fayl')),
                ('comment', models.TextField(blank=True, verbose_name='Izoh')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.assignment', verbose_name='Topshiriq')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="O'quvchi")),
            ],
            options={
                'verbose_name': 'Topshiriq javob',
                'verbose_name_plural': 'Topshiriq javoblar',
                'ordering': ['-submitted_at'],
                'unique_together': {('assignment', 'student')},
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(help_text='0 dan 50 gacha ball kiriting', verbose_name='Ball (0-50)')),
                ('comment', models.TextField(blank=True, verbose_name="O'qituvchi izohi")),
                ('graded_at', models.DateTimeField(auto_now_add=True)),
                ('submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.submission', verbose_name='Topshiriq javob')),
            ],
            options={
                'verbose_name': 'Baho',
                'verbose_name_plural': 'Baholar',
                'ordering': ['-graded_at'],
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Test nomi')),
                ('description', models.TextField(blank=True, verbose_name='Tavsif')),
                ('time_limit', models.IntegerField(default=30, verbose_name='Vaqt chegarasi (daqiqa)')),
                ('max_score', models.IntegerField(default=50, verbose_name='Maksimal ball')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Yaratuvchi')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subject', verbose_name='Fan')),
            ],
            options={
                'verbose_name': 'Test',
                'verbose_name_plural': 'Testlar',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(verbose_name='Savol matni')),
                ('option_a', models.CharField(max_length=200, verbose_name='A variant')),
                ('option_b', models.CharField(max_length=200, verbose_name='B variant')),
                ('option_c', models.CharField(max_length=200, verbose_name='C variant')),
                ('option_d', models.CharField(max_length=200, verbose_name='D variant')),
                ('correct_answer', models.CharField(choices=[('A', 'A variant'), ('B', 'B variant'), ('C', 'C variant'), ('D', 'D variant')], max_length=1, verbose_name="To'g'ri javob")),
                ('points', models.IntegerField(default=1, verbose_name='Ball qiymati')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='app.test', verbose_name='Test')),
            ],
            options={
                'verbose_name': 'Savol',
                'verbose_name_plural': 'Savollar',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(verbose_name='Olingan ball')),
                ('total_questions', models.IntegerField(verbose_name='Jami savollar')),
                ('correct_answers', models.IntegerField(verbose_name="To'g'ri javoblar")),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="O'quvchi")),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.test', verbose_name='Test')),
            ],
            options={
                'verbose_name': 'Test natijasi',
                'verbose_name_plural': 'Test natijalari',
                'ordering': ['-completed_at'],
                'unique_together': {('test', 'student')},
            },
        ),
    ]
