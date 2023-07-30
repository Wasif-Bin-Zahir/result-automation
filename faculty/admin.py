from django.contrib import admin
from . models import Final_MarkSheet_Viva_Course, Viva_Marks, Attendence_and_CT_Mark, Final_MarkSheet_Project_Course, Theory_Marks,Final_MarkSheet_Lab_Course, Lab_Marks, Lab_Final_50_Marks, Project_Marks, Research_Project_Marks

# Register your models here.
@admin.register(Attendence_and_CT_Mark)
class Attendence_and_CT_Mark_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'course_teacher', 'ct_marks', 'attendence_marks']

# theory
@admin.register(Theory_Marks)
class Theory_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'course_teacher', 'total_marks']

# lab marks
@admin.register(Lab_Marks)
class Lab_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'lab_total_mark']

# Lab_Final_50_Marks
@admin.register(Lab_Final_50_Marks)
class Lab_Final_50_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'total_mark']

# Project_Marks
@admin.register(Project_Marks)
class Project_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'total_mark']

# Research_Project_Marks
@admin.register(Research_Project_Marks)
class Research_Project_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'total_mark']

# Final_MarkSheet_Lab_Course
@admin.register(Final_MarkSheet_Lab_Course)
class Final_MarkSheet_Lab_Course_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'total_marks']

# Final_MarkSheet_Project_Course
@admin.register(Final_MarkSheet_Project_Course)
class Final_MarkSheet_Project_Course_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'total_marks']

# Viva_Marks
@admin.register(Viva_Marks)
class Viva_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'total_mark']

# Final_MarkSheet_Viva_Course
@admin.register(Final_MarkSheet_Viva_Course)
class Final_MarkSheet_Viva_Course(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'total_marks']