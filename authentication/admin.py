from django.contrib import admin
from authentication.models import Student, User, Teacher, Teacher_email, OfficeStuff, ExamController, ExamCommitte
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class UserModelAdmin(BaseUserAdmin):

    list_display = ('id', 'email', 'name', 'tc', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'tc')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'tc', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'id')
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)


@admin.register(Student)
class StudentModel(admin.ModelAdmin):
    list_display = ['first_name', 'student_id']


@admin.register(Teacher)
class TeacherModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']


@admin.register(Teacher_email)
class Teacher_email_ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']


@admin.register(OfficeStuff)
class OfficeStuff_ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']


@admin.register(ExamController)
class ExamController_ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']


@admin.register(ExamCommitte)
class ExamCommitte_ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
