from django.contrib import admin
from . models import Final_MarkSheet_ResearchProject_Course, External_teacher_marks, Send_To_Third_Examinner, Third_Examinner_Marks, External_Teacher_Research_Project_Marks, Third_Examinner_ResearchProject_Marks, Final_MarkSheet_Theory_Course
# Register your models here.

@admin.register(External_teacher_marks)
class External_teacher_marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code', 'marks']

@admin.register(Send_To_Third_Examinner)
class Send_To_Third_Examinner_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code', 'session']

@admin.register(Third_Examinner_Marks)
class Third_Examinner_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code', 'session', 'marks']

@admin.register(Third_Examinner_ResearchProject_Marks)
class Third_Examinner_ResearchProject_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code', 'session', 'marks']

@admin.register(External_Teacher_Research_Project_Marks)
class External_Teacher_Research_Project_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code', 'total_mark']

@admin.register(Final_MarkSheet_Theory_Course)
class Final_MarkSheet_Theory_Course_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code', 'GP']

@admin.register(Final_MarkSheet_ResearchProject_Course)
class Final_MarkSheet_ResearchProject_Course_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code', 'GP']
