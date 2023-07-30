from django.contrib import admin
from . models import Course, Running_Semester, Roll_Sheet, Teacher_Student_Info
from . models import Registration_By_Semester
from . models import Show_By_Semester
# Register your models here.


@admin.register(Registration_By_Semester)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['session', 'student_id',
                    'name_of_the_candidates', 'semester_name']

# Register your models here.


@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'course_teacher']


@admin.register(Running_Semester)
class Running_SemesterModelAdmin(admin.ModelAdmin):
    list_display = ['semester_no', 'session']


@admin.register(Roll_Sheet)
class Roll_Sheet_ModelAdmin(admin.ModelAdmin):
    list_display = ['session', 'student_id']


@admin.register(Teacher_Student_Info)
class Teacher_Student_Info_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code']


@admin.register(Show_By_Semester)
class Show_Student_Info_ModelAdmin(admin.ModelAdmin):
    list_display = ['session', 'student_id']
