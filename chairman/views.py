from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from authentication.models import *
from chairman.forms import CourseForm, Running_Semester_Form
from chairman.models import Course, Roll_Sheet, Running_Semester, Teacher_Student_Info, Registration_By_Semester
from authentication.forms import StudentRegForm, TeacherRegForm, OfficeStuffRegForm


# Create your views here.
def chairman_profile(request):
    if request.user.is_admin:
        return render(request, 'chairman/profile.html')
    else:
        return HttpResponseRedirect('/')


def chairman_password_reset(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            fm = PasswordChangeForm(request.user)
            if request.method == 'POST':
                fm = PasswordChangeForm(user=request.user, data=request.POST)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Password change successfully...')
                    update_session_auth_hash(request, fm.user)

                    return HttpResponseRedirect('/chairman/profile/')
            else:
                fm = PasswordChangeForm(request.user)
            return render(request, 'chairman/pswreset1.html', {'form': fm})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')


def chairman_password_reset2(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            if request.method == 'POST':
                fm = SetPasswordForm(user=request.user, data=request.POST)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Password change successfully...')
                    update_session_auth_hash(request, fm.user)
                    return HttpResponseRedirect('/chairman/profile/')
            else:
                fm = SetPasswordForm(request.user)
            return render(request, 'chairman/pswreset2.html', {'form': fm})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')


# logout
def chairman_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')


def teacher_list(request):
    if request.user.is_admin:
        teachers = Teacher.objects.all()
        return render(request, 'chairman/teacher_list.html', {'teachers': teachers})
    else:
        return HttpResponseRedirect('/')


def add_courses(request):
    allCourses = Course.objects.all()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course Added Successfull!!')
            return HttpResponseRedirect('/chairman/add_courses/')
        else:
            messages.warning(request, 'Your Enter Data is not Correct. Please re-enter again....')
            return HttpResponseRedirect('/chairman/add_courses/')
    form = CourseForm()
    return render(request, 'chairman/add_courses.html', {'form': form, 'courses': allCourses})


def chairman_teacher_reg(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = TeacherRegForm(request.POST, request.FILES)
            if form.is_valid():
                mail = form.cleaned_data['email']
                flag = False
                for m in Teacher_email.objects.all():
                    if m.email == mail:
                        flag = True
                        break
                if flag == True:
                    messages.success(request, 'Successfully create a Faculty Member')
                    messages.success(request, 'Activate your account from email')
                    return HttpResponseRedirect('/')

            else:
                messages.info(request, 'Enter the correct value!!!')
        form = TeacherRegForm()
        return render(request, 'chairman/teacher_signup.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def delete_faculty_page(request):
    faculty_members = Teacher.objects.all()
    return render(request, 'chairman/deleteFacultyPage.html', {'faculty_members': faculty_members})


def delete_current_faculty(request, faculty_id):
    if request.user.is_admin:
        data = Teacher.objects.get(id=faculty_id)
        # data.delete()
        messages.success(request, 'Faculty member deleted successfully')
        return HttpResponseRedirect('/chairman/delete_faculty_page/')
    else:
        return HttpResponseRedirect('/')


def chairman_student_reg(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = StudentRegForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'A Student added successfully!!!!')
                return HttpResponseRedirect('/chairman/profile/')
            else:
                messages.warning(request, 'Enter the correct data to registration!!!')
                return HttpResponseRedirect('/chairman_student_reg')
        form = StudentRegForm()
        return render(request, 'chairman/student_signup.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def delete_student_page(request):
    if request.user.is_admin:
        students = Student.objects.all()
        return render(request, 'chairman/student_list.html', {'students': students})
    else:
        return HttpResponseRedirect('/')


def delete_current_student(request, student_id):
    if request.user.is_admin:
        data = Student.objects.get(id=student_id)
        # data.delete()
        data = (data.student_id)
        messages.success(request, ' student deleted successfully', {data})
        return HttpResponseRedirect('/chairman/delete_student_page/')
    else:
        return HttpResponseRedirect('/')


def delete_stuff_page(request):
    if request.user.is_admin:
        stuffs = OfficeStuff.objects.all()
        return render(request, 'chairman/stuff_list.html', {'stuffs': stuffs})
    else:
        return HttpResponseRedirect('/')


def delete_current_stuff(request, stuff_id):
    if request.user.is_admin:
        data = OfficeStuff.objects.get(id=stuff_id)
        # data.delete()
        data = (data.first_name + data.last_name)
        messages.warning(request, 'requested stuff deleted successfully', {data})
        return HttpResponseRedirect('/chairman/delete_stuff_page/')
    else:
        return HttpResponseRedirect('/')


def chairman_stuff_reg(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = OfficeStuffRegForm(request.POST, request.FILES)
            if form.is_valid():
                # form.save()
                messages.success(request, 'A stuff account created successfully')
                return HttpResponseRedirect('/chairman/profile/')

            else:
                messages.info(request, 'Enter the correct value!!!')
        form = OfficeStuffRegForm()
        return render(request, 'chairman/officestuff_signup.html', {'form': form})
    return HttpResponseRedirect('/')


def add_semesters(request):
    if request.user.is_admin:
        Running_Semesters = Running_Semester.objects.all()
        form = Running_Semester_Form()
        if request.method == 'POST':
            form = Running_Semester_Form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'semester added successfully')
                return HttpResponseRedirect('/chairman/add_semesters/')
            else:
                messages.warning(request, 'Enter the correct data!!!')
                return HttpResponseRedirect('/chairman/add_semesters/')
        else:
            return render(request, 'chairman/add_semesters.html',
                          {'form': form, 'Running_Semesters': Running_Semesters})
    else:
        return HttpResponseRedirect('/')


def show_roll_sheet(request, semester_no='1st Year 1st Semester'):
    students_regular = Registration_By_Semester.objects.filter(semester_name=semester_no, remarks='Regular').order_by(
        'student_id')
    students_backlog = Registration_By_Semester.objects.filter(semester_name=semester_no, remarks='BackLog').order_by(
        'student_id')
    students_special = Registration_By_Semester.objects.filter(semester_name=semester_no, remarks='Special').order_by(
        'student_id')
    course_codes = Course.objects.filter(semister_no=semester_no)
    individual_student_c_codes = Teacher_Student_Info.objects.filter(semester=semester_no)
    backLog_students_and_courses = {}
    special_students_and_courses = {}
    count = 0
    for c in course_codes:
        count += 1
    student_count = 0
    for cnt in students_regular:
        student_count += 1
    # backlog students and courses
    for student in students_backlog:
        mylist = []
        for code in individual_student_c_codes:
            if student.student_id == code.student_id:
                mylist.append(code.course_code)
        final_list = []
        for c in course_codes:
            flag = False
            for l in mylist:
                if c.course_code == l:
                    flag = True
            if flag == True:
                final_list.append(c.course_code)
            else:
                final_list.append(" ")
        student_count += 1
        backLog_students_and_courses[student] = {'course_list': final_list, 'index': student_count}

    # specail students and courses
    for student in students_special:
        mylist = []
        for code in individual_student_c_codes:
            if student.student_id == code.student_id:
                mylist.append(code.course_code)
        final_list = []
        for c in course_codes:
            flag = False
            for l in mylist:
                if c.course_code == l:
                    flag = True
            if flag == True:
                final_list.append(c.course_code)
            else:
                final_list.append(" ")
        special_students_and_courses[student] = final_list

    context = {
        'students_backlog': students_backlog,
        'students_regular': students_regular,
        'course_codes': course_codes,
        'semester_no': semester_no,
        'count': count,
        'individual_student_c_codes': individual_student_c_codes,
        'backLog_students_and_courses': backLog_students_and_courses,
        'special_students_and_courses': special_students_and_courses,
    }

    return render(request, 'chairman/show_roll_sheet.html', context)
