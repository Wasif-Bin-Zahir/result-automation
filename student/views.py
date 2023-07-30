from authentication.models import *
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserChangeForm
from chairman.models import Course, Running_Semester, Roll_Sheet, Teacher_Student_Info, Registration_By_Semester


def student_profile(request):
    if request.user.is_authenticated:
        student = Student.objects.get(email= request.user)
        res = Student.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            return render(request, 'student/profile.html', {'student': student})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

#logout
def student_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')


def student_password_reset(request):
    if request.user.is_authenticated:
        res = Student.objects.filter(email= request.user)
        student = Student.objects.get(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            fm = PasswordChangeForm(request.user)
            if request.method == 'POST':
                fm = PasswordChangeForm(user = request.user, data = request.POST)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Password change successfully...')
                    update_session_auth_hash(request, fm.user)
                    return HttpResponseRedirect('/student/profile/')
            else:
                fm = PasswordChangeForm(request.user)
            return render(request, 'student/pswreset1.html', {'form': fm, 'student': student})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/') 

def student_password_reset2(request):
    if request.user.is_authenticated:
        student = Student.objects.get(email= request.user)
        res = Student.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            if request.method == 'POST':
                fm = SetPasswordForm(user= request.user, data= request.POST)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Password change successfully...')
                    update_session_auth_hash(request, fm.user)
                    return HttpResponseRedirect('/student/profile/')
            else:
                fm = SetPasswordForm(request.user)
            return render(request, 'student/pswreset2.html', {'form': fm, 'student': student})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

def current_courses(request):
    if request.user.is_authenticated:
        student = Student.objects.get(email= request.user)
        k = student.session
        running_semester = Running_Semester.objects.filter(session= k)
        flag = False
        for r in running_semester:
            semester = r.semester_no
            flag = True
        if flag == False:
            return HttpResponse('You are special student')
        courses = Course.objects.filter(semister_no = semester)
        return render(request, 'student/current_courses.html', {'courses': courses, 'student':student})
    else:
        return HttpResponseRedirect('/')

def complete_courses(request):
    student = Student.objects.get(email= request.user)
    k = student.session
    running_semester = Running_Semester.objects.filter(session= k)
    flag = False
    for r in running_semester:
        semester = r.semester_no
        flag = True
    if flag == False:
        return HttpResponse('You are special student')
    for r in running_semester:
        semester = r.semester_no
    if semester == '4th Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester)
    if semester == '4th Year 1st Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester')
    if semester == '3rd Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester')
    if semester == '3rd Year 1st Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester')
    if semester == '2nd Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester')
    if semester == '2nd Year 1st Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester').exclude(semister_no= '2nd Year 2nd Semester')
    if semester == '1st Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester').exclude(semister_no= '2nd Year 1st Semester')
    if semester == '1st Year 1st Semester':
        courses = Course.objects.all()
    return render(request, 'student/complete_courses.html', {'courses': courses, 'student':student})

def course_registration(request):
    student = Student.objects.get(email= request.user)
    session= student.session
    semester = Running_Semester.objects.filter(session = session)
    find_sem = False
    for s in semester:
        sem = s.semester_no
        find_sem = True
    
    if find_sem == False:
        return HttpResponseRedirect('/student/student_special_course_registration/')

    courses = Course.objects.filter(semister_no = sem)
    course_code = []
    running_semester = Running_Semester.objects.filter(session= student.session)
    for r in running_semester:
        semester = r.semester_no
    if semester == '4th Year 2nd Semester':
        bl_courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '2nd Year 2nd Semester').exclude(semister_no= '1st Year 2nd Semester')
        backLogSemester = ['1st Year 1st Semester', '2nd Year 1st Semester', '3rd Year 1st Semester', '4th Year 1st Semester']
    if semester == '4th Year 1st Semester':
        bl_courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '2nd Year 2nd Semester').exclude(semister_no= '1st Year 2nd Semester')
        backLogSemester = ['1st Year 1st Semester', '2nd Year 1st Semester', '3rd Year 1st Semester']
    if semester == '3rd Year 2nd Semester':
       bl_courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 1st Semester').exclude(semister_no= '2nd Year 1st Semester').exclude(semister_no= '1st Year 1st Semester')
       backLogSemester = ['1st Year 2nd Semester', '2nd Year 2nd Semester']
    if semester == '3rd Year 1st Semester':
        bl_courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '2nd Year 2nd Semester').exclude(semister_no= '1st Year 2nd Semester')
        backLogSemester = ['1st Year 1st Semester', '2nd Year 1st Semester']
    if semester == '2nd Year 2nd Semester':
        bl_courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester').exclude(semister_no= '1st Year 1st Semester').exclude(semister_no= '2nd Year 1st Semester')
        backLogSemester = ['1st Year 2nd Semester']
    if semester == '2nd Year 1st Semester':
        bl_courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester').exclude(semister_no= '2nd Year 2nd Semester').exclude(semister_no= '1st Year 2nd Semester')
        backLogSemester = ['1st Year 1st Semester']
    if semester == '1st Year 2nd Semester':
        bl_courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester').exclude(semister_no= '2nd Year 1st Semester').exclude(semister_no= '2nd Year 2nd Semester').exclude(semister_no= '1st Year 1st Semester')
        backLogSemester=[]
    if semester == '1st Year 1st Semester':
        bl_courses = None
        backLogSemester = []
    backlog_course_code = []
    if request.method == 'POST':

        session = student.session
        student_id = student.student_id
        name_of_student = student.first_name + " " + student.last_name
        hall = student.hall
        remarks = 'Regular'

        #credit count
        total_credit = 0
        for course in courses:
            credit = course.credit
            total_credit += credit
        if bl_courses is not None:
            for b in bl_courses:
                c_code = b.course_code
                form_data = request.POST.get(f'{c_code}')
                if form_data is not None:
                    total_credit += b.credit
                    if total_credit > 30:
                        messages.warning(request,'Course credit can not greater than 30. Make sure you take less than or equal to 30 credit. Try again!!!!!')
                        return HttpResponseRedirect('/student/course_registration/')
        #regular course add to teacher
        for course in courses:
            course_code.append((course.course_code))
            c_code = course.course_code
            current_course = Course.objects.get(course_code = c_code)
            teacher = (current_course.course_teacher)
            credit = current_course.credit
            semister_no = current_course.semister_no
            course_name = current_course.course_name
            data = Teacher_Student_Info(
                student_name = name_of_student,
                student_id = student_id,
                course_name = course_name,
                course_code = c_code,
                teacher = teacher,
                hall = hall,
                session = session,
                credit = credit,
                remarks= 'Regular',
                semester = semister_no,
            )

            #registration by semester
            chek_reg_by_sem_student = Registration_By_Semester.objects.filter(student_id= student_id, semester_name= semister_no)
            flag = False
            for c in chek_reg_by_sem_student:
                flag = True
            if flag == False:
                reg_by_sem = Registration_By_Semester(session= session, student_id= student_id, name_of_the_candidates= name_of_student, hall= hall, semester_name= semister_no, remarks= remarks)
                reg_by_sem.save()


            check_teacher_stu = Teacher_Student_Info.objects.filter(student_name= name_of_student, course_code = c_code, teacher = teacher)
            flag = False
            for check in check_teacher_stu:
                flag = True
            if flag == True:
                messages.warning(request,'You are already registered these courses!!!')
                return HttpResponseRedirect('/student/course_registration/')
            else:
                data.save()
                # messages.success(request, 'course added successfully to the teacher')
        
        #backlog course information add to teacher
        if bl_courses is not None:
            for backLogCourseCode in  bl_courses:
                c_code = backLogCourseCode.course_code
                course_code.append(c_code)
                teacher = backLogCourseCode.course_teacher
                credit = backLogCourseCode.credit
                semister_no = backLogCourseCode.semister_no
                course_name = backLogCourseCode.course_name
                remarks = 'BackLog'
                form_data = request.POST.get(f'{c_code}')
                if form_data is not None:
                    # registration by semester
                    chek_reg_by_sem_student = Registration_By_Semester.objects.filter(student_id= student_id, semester_name= semister_no)
                    flag = False
                    for c in chek_reg_by_sem_student:
                        flag = True
                    if flag == False:
                        reg_by_sem = Registration_By_Semester(session= session, student_id= student_id, name_of_the_candidates= name_of_student, hall= hall, semester_name= semister_no, remarks= remarks)
                        reg_by_sem.save()

                    data = Teacher_Student_Info(
                        student_name = name_of_student,
                        student_id = student_id,
                        course_name = course_name,
                        course_code = c_code,
                        teacher = teacher,
                        hall = hall,
                        session = session,
                        credit = credit,
                        remarks= remarks,
                        semester = semister_no,
                    )
                    check_teacher_stu = Teacher_Student_Info.objects.filter(student_name= name_of_student, course_code = c_code, teacher = teacher)
                    flag = False
                    for check in check_teacher_stu:
                        flag = True
                    if flag == True:
                        messages.warning(request, 'You are already registered these courses!!!')
                        return HttpResponseRedirect('/student/course_registration/')
                    else:
                        data.save()
                        # messages.success(request, 'course added successfully to the teacher')


        check = Roll_Sheet.objects.filter(student_id= student_id)
        flag = False
        for c in check:
            flag = True
        if flag == True:
            messages.warning(request, 'You are already registered in this semester!!!')
        else:
            data = Roll_Sheet(session= session, student_id= student_id, name_of_student= name_of_student, hall= hall, course_code= course_code, remarks= remarks, semester=semister_no)
            messages.success(request, 'Your Registration is successfull!!!')
            data.save()
    

    return render(request, 'student/course_registration.html',{'student':student, 'sem': sem, 'courses': courses, 'bl_courses': bl_courses, 'backLogSemester': backLogSemester})

def student_special_course_registration(request):
    student = Student.objects.get(email= request.user)
    student_id = student.student_id
    name_of_student = student.first_name + " " + student.last_name
    session= student.session
    hall = student.hall
    semesters = Running_Semester.objects.all()
    backLogCourses = []
    specialCourses = []
    specialSemesters = []
    all_semesters = ['1st Year 1st Semester', '1st Year 2nd Semester',
    '2nd Year 1st Semester', '2nd Year 2nd Semester', '3rd Year 1st Semester',
    '3rd Year 2nd Semester', '4th Year 1st Semester', '4th Year 2nd Semester']
    for semester in semesters:
        courses = Course.objects.filter(semister_no= semester.semester_no)
        for course in courses:
            backLogCourses.append(course)
    
    for x in all_semesters:
        flag = True
        for semester in semesters:
            if x == semester.semester_no:
                flag = False
        if flag:
            courses = Course.objects.filter(semister_no= x)
            for course in courses:
                specialCourses.append(course)
            specialSemesters.append(x)
            
    # print(semesters)
    courses = Course.objects.filter()
    context = {
        'session': session,
        'student': student,
        'backLogCourses': backLogCourses,
        'specialCourses': specialCourses,
        'backLogSemester': semesters,
        'specialSemester': specialSemesters,
    }
    if request.method == 'POST':
        course_code = []
        #credit count
        total_credit = 0
        for b_course in backLogCourses:
            course = request.POST.get(f'{b_course.course_code}')
            if course is not None:
                course = Course.objects.get(course_code = course)
                credit = course.credit
                total_credit += credit
        for sp_course in specialCourses:
            course = request.POST.get(f'{sp_course.course_code}')
            if course is not None:
                course = Course.objects.get(course_code = course)
                credit = course.credit
                total_credit += credit
        if total_credit > 30:
            messages.warning(request, 'You can not take more than 30 Credits!!!')
            return HttpResponseRedirect('/student/student_special_course_registration/')

        for b_course in backLogCourses:
            course = request.POST.get(f'{b_course.course_code}')
            if course is not None:
                course = Course.objects.get(course_code = course)
                c_code = course.course_code
                course_code.append(c_code)
                teacher = course.course_teacher
                credit = course.credit
                semister_no = course.semister_no
                course_name = course.course_name
                remarks = 'BackLog'
                form_data = request.POST.get(f'{b_course.course_code}')
                if form_data is not None:
                    # registration by semester
                    chek_reg_by_sem_student = Registration_By_Semester.objects.filter(student_id= student_id, semester_name= semister_no)
                    flag = False
                    for c in chek_reg_by_sem_student:
                        flag = True
                    if flag == False:
                        reg_by_sem = Registration_By_Semester(session= session, student_id= student_id, name_of_the_candidates= name_of_student, hall= hall, semester_name= semister_no, remarks= remarks)
                        reg_by_sem.save()

                    data = Teacher_Student_Info(
                        student_name = name_of_student,
                        student_id = student_id,
                        course_name = course_name,
                        course_code = c_code,
                        teacher = teacher,
                        hall = hall,
                        session = session,
                        credit = credit,
                        remarks= remarks,
                        semester = semister_no,
                    )
                    check_teacher_stu = Teacher_Student_Info.objects.filter(student_name= name_of_student, course_code = c_code, teacher = teacher)
                    flag = False
                    for check in check_teacher_stu:
                        flag = True
                    if flag == True:
                        messages.warning(request, 'You are already registered these courses!!!')
                        return HttpResponseRedirect('/student/course_registration/')
                    else:
                        data.save()

        for sp_course in specialCourses:
            course = request.POST.get(f'{sp_course.course_code}')
            if course is not None:
                course = Course.objects.get(course_code = course)
                c_code = course.course_code
                course_code.append(c_code)
                teacher = course.course_teacher
                credit = course.credit
                semister_no = course.semister_no
                course_name = course.course_name
                remarks = 'Special'
                form_data = request.POST.get(f'{sp_course.course_code}')
                if form_data is not None:
                    # registration by semester
                    chek_reg_by_sem_student = Registration_By_Semester.objects.filter(student_id= student_id, semester_name= semister_no)
                    flag = False
                    for c in chek_reg_by_sem_student:
                        flag = True
                    if flag == False:
                        reg_by_sem = Registration_By_Semester(session= session, student_id= student_id, name_of_the_candidates= name_of_student, hall= hall, semester_name= semister_no, remarks= remarks)
                        reg_by_sem.save()

                    data = Teacher_Student_Info(
                        student_name = name_of_student,
                        student_id = student_id,
                        course_name = course_name,
                        course_code = c_code,
                        teacher = teacher,
                        hall = hall,
                        session = session,
                        credit = credit,
                        remarks= remarks,
                        semester = semister_no,
                    )
                    check_teacher_stu = Teacher_Student_Info.objects.filter(student_name= name_of_student, course_code = c_code, teacher = teacher)
                    flag = False
                    for check in check_teacher_stu:
                        flag = True
                    if flag == True:
                        messages.warning(request, 'You are already registered these courses!!!')
                        return HttpResponseRedirect('/student/course_registration/')
                    else:
                        data.save()

        check = Roll_Sheet.objects.filter(student_id= student_id)
        flag = False
        for c in check:
            flag = True
        if flag == True:
            messages.warning(request, 'You are already registered in this semester!!!')
        else:
            data = Roll_Sheet(session= session, student_id= student_id, name_of_student= name_of_student, hall= hall, course_code= course_code, remarks= remarks, semester=semister_no)
            messages.success(request, 'Your Registration is successfull!!!')
            data.save()

    return render(request, 'student/special_course_registration.html', context)

def application_form(request):
    return render(request, 'student/application_form.html')