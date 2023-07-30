import math
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from requests import request
from authentication.models import *
from chairman.models import Course, Teacher_Student_Info
from . models import Final_MarkSheet_Viva_Course, Viva_Marks, Final_MarkSheet_Project_Course, Final_MarkSheet_Lab_Course, Attendence_and_CT_Mark, Lab_Final_50_Marks, Theory_Marks, Lab_Marks, Project_Marks, Research_Project_Marks
# Create your views here.


def faculty_profile(request):
    if request.user.is_authenticated:
        res = Teacher.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            return render(request, 'faculty/profile.html', {'faculty': res})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')


def faculty_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')


def faculty_pswreset(request):
    if request.user.is_authenticated:
        res = Teacher.objects.filter(email= request.user)
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
                    return HttpResponseRedirect('/faculty/profile/')
            else:
                fm = PasswordChangeForm(request.user)
            return render(request, 'faculty/pswreset1.html', {'form': fm, 'faculty': res})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/') 

def faculty_pswreset2(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            res = Teacher.objects.filter(email= request.user)
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
                        return HttpResponseRedirect('/faculty/profile/')
                else:
                    fm = SetPasswordForm(request.user)
                return render(request, 'faculty/pswreset2.html', {'form': fm, 'faculty': res})
            else:
                return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')


def current_course(request):
    if request.user.is_authenticated:
        all_semesters = ['1st Year 1st Semester', '1st Year 2nd Semester',
                        '2nd Year 1st Semester', '2nd Year 2nd Semester', '3rd Year 1st Semester',
                        '3rd Year 2nd Semester', '4th Year 1st Semester', '4th Year 2nd Semester']
        user = request.user
        faculty = Teacher.objects.filter(email= request.user)
        courses = Course.objects.filter(course_teacher = user)
        all_semester_list = []
        for semester in all_semesters:
            c_list = []
            flag = False
            for course in courses:
                if semester == course.semister_no:
                    c_list.append(course.course_code)
                    flag = True
            if flag == True:
                all_semester_list.append(semester)
        context = {
            'courses': courses, 
            'faculty': faculty, 
            'all_semesters': all_semester_list,
            }
        return render(request, 'faculty/current_course.html', context)
    else:
        return HttpResponseRedirect('/')



def course_details(request, course_code):
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Special').order_by('student_id')
    course = Course.objects.get(course_code= course_code)
    if course.course_type == 'Lab':
        return HttpResponseRedirect(f'/faculty/lab_course_details/{course.course_code}/')
    if course.course_type == 'Project':
        return HttpResponseRedirect(f'/faculty/project_course_details/{course.course_code}/')
    if course.course_type == 'Research_Project':
        return HttpResponseRedirect(f'/faculty/research_project_course_details/{course.course_code}/')
    if course.course_type == 'Viva':
        return HttpResponseRedirect(f'/faculty/viva_project_course_details/{course.course_code}/')
    c_code = (course.course_code)
    c_name = (course.course_name)
    c_credit = (course.credit)
    c_teacher = course.course_teacher
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    for stu in backLog_students:
        count += 1
        backLogStudents[stu] = count
    context = {
        'c_code': c_code,
        'c_name': c_name,
        'c_credit': c_credit,
        'regular_students': regular_students,
        'c_teacher': c_teacher,
        'backLogStudents': backLogStudents,
        'special_students': special_students,
    }
    return render(request, 'faculty/course_details.html', context)


def lab_course_details(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    for stu in backLog_students:
        count += 1
        backLogStudents[stu] = count
    context = {
    'c_code' : (course.course_code),
    'c_name' : (course.course_name),
    'c_credit' : (course.credit),
    'c_teacher' : course.course_teacher,
    'regular_students': regular_students,
    'backLogStudents': backLogStudents,
    'special_students': special_students,
    }
    return render(request, 'faculty/lab_course_details.html', context)

def attendence_sheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    for stu in backLog_students:
        count += 1
        backLogStudents[stu] = count
    print(backLogStudents)
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_students': regular_students,
        'backLogStudents': backLogStudents,
        'special_students': special_students,
    }
    return render(request, 'faculty/attendence_sheet.html', context)

def ct_and_attendence_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    regularStudents = {}
    specialStudents = {}
    for stu in regular_students:
        student_details = {}
        ct_attend_marks = Attendence_and_CT_Mark.objects.filter(student_id= stu.student_id, course_code= course_code)
        ct_marks = 0
        attendence_mark = 0
        for c in ct_attend_marks:
            ct_marks = c.ct_marks 
            attendence_mark = c.attendence_marks
        student_details['ct_marks'] = ct_marks
        student_details['attendence_mark'] = attendence_mark
        regularStudents[stu] = student_details
        count += 1
    for stu in backLog_students:
        student_details = {}
        ct_attend_marks = Attendence_and_CT_Mark.objects.filter(student_id= stu.student_id, course_code= course_code)
        ct_marks = 0
        attendence_mark = 0
        for c in ct_attend_marks:
            ct_marks = c.ct_marks 
            attendence_mark = c.attendence_marks
        count += 1
        student_details['ct_marks'] = ct_marks
        student_details['attendence_mark'] = attendence_mark
        student_details['count'] = count
        backLogStudents[stu] = student_details
    for stu in special_students:
        student_details = {}
        ct_attend_marks = Attendence_and_CT_Mark.objects.filter(student_id= stu.student_id, course_code= course_code)
        ct_marks = 0
        attendence_mark = 0
        for c in ct_attend_marks:
            ct_marks = c.ct_marks 
            attendence_mark = c.attendence_marks
        count += 1
        student_details['ct_marks'] = ct_marks
        student_details['attendence_mark'] = attendence_mark
        student_details['count'] = count
        specialStudents[stu] = student_details
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regularStudents': regularStudents,
        'ct_attend_marks': ct_attend_marks,
        'backLogStudents': backLogStudents,
        'specialStudents': specialStudents,
        }
    if request.method == 'POST':
        course = Course.objects.get(course_code= course_code)
        students = Teacher_Student_Info.objects.filter(course_code= course_code)
        ct_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code)

        for student in students:
            ct_marks = request.POST.get(f'ct_marks_{student.student_id}')
            attend_marks = request.POST.get(f'attendence_mark_{student.student_id}')
            if ct_marks and attend_marks:
                ct_marks = (float(ct_marks))
                attend_marks = (float(attend_marks))
                if ct_marks > 20 or attend_marks > 10:
                    messages.warning(request, 'ct marks can not greater than 20 and attendence mark can not grater than 10')
                    return HttpResponseRedirect(f'/faculty/ct_and_attendence_mark/{course_code}/')       
            else:
                ct_marks = 0
                attend_marks = 0
            student_id = student.student_id
            student_name = student.student_name
            session = student.session
            semester_no = course.semister_no
            course_code = course_code
            course_name = course.course_name
            course_teacher = course.course_teacher
            credit = course.credit
            remarks = student.remarks
            ct_marks = ct_marks
            attendence_marks = attend_marks
            total_ct_and_attendence_marks = ct_marks + attendence_marks
            checker = Attendence_and_CT_Mark.objects.filter(student_id= student_id, course_code=course_code, course_teacher= course.course_teacher)
            flag = False
            for c in checker:
                id = c.id
                data = Attendence_and_CT_Mark(id=id,student_id = student_id,student_name = student_name,session = session,semester_no = semester_no,course_code = course_code,course_name = course_name,course_teacher = course_teacher,credit = credit,remarks =remarks,ct_marks = ct_marks,attendence_marks = attendence_marks,total_ct_and_attendence_marks = total_ct_and_attendence_marks)
                data.save()
                flag = True
            if flag == False:
                data = Attendence_and_CT_Mark(
                    student_id = student_id,
                    student_name = student_name,
                    session = session,
                    semester_no = semester_no,
                    course_code = course_code,
                    course_name = course_name,
                    course_teacher = course_teacher,
                    credit = credit,
                    remarks =remarks,
                    ct_marks = ct_marks,
                    attendence_marks = attendence_marks,
                    total_ct_and_attendence_marks = total_ct_and_attendence_marks
                    )
                data.save()
        messages.success(request,'CT and Attendence Mark Added Successfully!!!!')
        return HttpResponseRedirect(f'/faculty/student_ct_and_attendence_mark/{course_code}/')  
    return render(request, 'faculty/ct_and_attendence_mark.html', context)

def student_ct_and_attendence_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_student_ct_and_attend_marks:
        count += 1
    for stu in backLog_student_ct_and_attend_marks:
        count += 1
        backLogStudents[stu] = count
    context = {
        'course_code': course_code,
        'course_name': course.course_name,
        'credit': course.credit,
        'semester_no': course.semister_no,
        'course_teacher': course.course_teacher,
        'regular_student_ct_and_attend_marks': regular_student_ct_and_attend_marks,
        'backLogStudents': backLogStudents,
        'special_student_ct_and_attend_marks': special_student_ct_and_attend_marks,
    }
    return render(request, 'faculty/student_ct_and_attendence_mark.html', context)

def edit_ct_and_attendence_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_student_ct_and_attend_marks:
        count += 1
    for stu in backLog_student_ct_and_attend_marks:
        count += 1
        backLogStudents[stu] = count
    context = {
        'course_code': course_code,
        'course_name': course.course_name,
        'credit': course.credit,
        'semester_no': course.semister_no,
        'course_teacher': course.course_teacher,
        'regular_student_ct_and_attend_marks': regular_student_ct_and_attend_marks,
        'backLogStudents': backLogStudents,
        'special_student_ct_and_attend_marks': special_student_ct_and_attend_marks,
    }
    if request.method == 'POST':
        course = Course.objects.get(course_code= course_code)
        students = Teacher_Student_Info.objects.filter(course_code= course_code)
        ct_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code)
        context = {
            'semister_no': course.semister_no,
            'c_code': course_code,
            'c_teacher': course.course_teacher,
            'credit': course.credit,
            'c_name': course.course_name,
            'students': students,
            'ct_attend_marks': ct_attend_marks,
            }
        for student in students:
            ct_marks = request.POST.get(f'{student.student_id}')
            attend_marks = request.POST.get(f'{student.student_name}')
            if ct_marks and attend_marks:
                ct_marks = (float(ct_marks))
                attend_marks = (float(attend_marks))
                if ct_marks > 20 or attend_marks > 10:
                    messages.warning(request, 'ct marks can not greater than 20 and attendence mark can not grater than 10')
                    return HttpResponseRedirect(f'/faculty/edit_ct_and_attendence_mark/{course_code}/')       
            else:
                ct_marks = 0
                attend_marks = 0
            student_id = student.student_id
            student_name = student.student_name
            session = student.session
            semester_no = course.semister_no
            course_code = course_code
            course_name = course.course_name
            course_teacher = course.course_teacher
            credit = course.credit
            remarks = student.remarks
            ct_marks = ct_marks
            attendence_marks = attend_marks
            total_ct_and_attendence_marks = ct_marks + attendence_marks
            checker = Attendence_and_CT_Mark.objects.filter(student_id= student_id, course_code=course_code, course_teacher= course.course_teacher)
            flag = False
            for c in checker:
                id = c.id
                data = Attendence_and_CT_Mark(id=id,student_id = student_id,student_name = student_name,session = session,semester_no = semester_no,course_code = course_code,course_name = course_name,course_teacher = course_teacher,credit = credit,remarks =remarks,ct_marks = ct_marks,attendence_marks = attendence_marks,total_ct_and_attendence_marks = total_ct_and_attendence_marks)
                data.save()
                flag = True
            if flag == False:
                data = Attendence_and_CT_Mark(
                    student_id = student_id,
                    student_name = student_name,
                    session = session,
                    semester_no = semester_no,
                    course_code = course_code,
                    course_name = course_name,
                    course_teacher = course_teacher,
                    credit = credit,
                    remarks =remarks,
                    ct_marks = ct_marks,
                    attendence_marks = attendence_marks,
                    total_ct_and_attendence_marks = total_ct_and_attendence_marks
                    )
                data.save()
        messages.success(request,'CT and Attendence Mark Added Successfully!!!!')
        return HttpResponseRedirect(f'/faculty/student_ct_and_attendence_mark/{course_code}/') 
    return render(request, 'faculty/edit_ct_and_attendence_mark.html', context)

def Theory_mark_sheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
    count = 0
    backLogStudents = {}
    regularStudents = {}
    specialStudents = {}
    for stu in regular_students:
        student_details = {}
        theory_marks = Theory_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        q1 = 0
        q2 = 0
        q3=0
        q4=0
        q5=0
        q6=0
        q7=0
        q8=0
        q9=0
        for c in theory_marks:
            q1 = c.q1 
            q2 = c.q2 
            q3 = c.q3 
            q4 = c.q4 
            q5 = c.q5 
            q6 = c.q6 
            q7 = c.q7 
            q8 = c.q8 
            q9 = c.q9 
        student_details['q1'] = q1
        student_details['q2'] = q2
        student_details['q3'] = q3
        student_details['q4'] = q4
        student_details['q5'] = q5
        student_details['q6'] = q6
        student_details['q7'] = q7
        student_details['q8'] = q8
        student_details['q9'] = q9
        regularStudents[stu] = student_details
        count += 1
    for stu in backLog_students:
        student_details = {}
        theory_marks = Theory_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        q1=0
        q2=0
        q3=0
        q4=0
        q5=0
        q6=0
        q7=0
        q8=0
        q9=0
        for c in theory_marks:
            q1 = c.q1 
            q2 = c.q2 
            q3 = c.q3 
            q4 = c.q4 
            q5 = c.q5 
            q6 = c.q6 
            q7 = c.q7 
            q8 = c.q8 
            q9 = c.q9 
        student_details['q1'] = q1
        student_details['q2'] = q2
        student_details['q3'] = q3
        student_details['q4'] = q4
        student_details['q5'] = q5
        student_details['q6'] = q6
        student_details['q7'] = q7
        student_details['q8'] = q8
        student_details['q9'] = q9
        count += 1
        student_details['count'] = count
        backLogStudents[stu] = student_details
    for stu in special_students:
        student_details = {}
        theory_marks = Theory_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        q1 = 0
        q2 = 0
        q3 = 0
        q4 = 0
        q5 = 0
        q6 = 0
        q7 = 0
        q8 = 0
        q9 = 0
        for c in theory_marks:
            q1 = c.q1 
            q2 = c.q2 
            q3 = c.q3 
            q4 = c.q4 
            q5 = c.q5 
            q6 = c.q6 
            q7 = c.q7 
            q8 = c.q8 
            q9 = c.q9 
        student_details['q1'] = q1
        student_details['q2'] = q2
        student_details['q3'] = q3
        student_details['q4'] = q4
        student_details['q5'] = q5
        student_details['q6'] = q6
        student_details['q7'] = q7
        student_details['q8'] = q8
        student_details['q9'] = q9
        count += 1
        student_details['count'] = count
        specialStudents[stu] = student_details
    if request.method == 'POST':
        for student in regular_students:
            total_marks = 0
            count = 0
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/detailed_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        for student in backLog_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/detailed_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        for student in special_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/detailed_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        
        messages.success(request, 'Theory Marks added/updated successfully')
        return HttpResponseRedirect(f'/faculty/show_theory_marks/{course_code}/')
            
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'credit': course.credit,
        'c_name': course.course_name,
        'regularStudents': regularStudents,
        'backLogStudents': backLogStudents,
        'specialStudents': specialStudents,
        }
    return render(request, 'faculty/detailed_mark_sheet.html', context)

def show_theory_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students_marks = Theory_Marks.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
    backLog_students_marks = Theory_Marks.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
    special_students_marks = Theory_Marks.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students_marks:
        count += 1
    for stu in backLog_students_marks:
        count += 1
        backLogStudents[stu] = count
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_students_marks': regular_students_marks,
        'backLogStudents': backLogStudents,
        'special_students_marks': special_students_marks,
        }
    return render(request, 'faculty/show_theory_marks.html', context)

def update_theory_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students_theory_marks = Theory_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students_theory_marks = Theory_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students_theory_marks = Theory_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students_theory_marks:
        count += 1
    for stu in backLog_students_theory_marks:
        count += 1
        backLogStudents[stu] = count
    
    if request.method == 'POST':
        regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
        backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
        special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
        for student in regular_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/Theory_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        for student in backLog_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/Theory_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        for student in special_students:
            total_marks = 0
            count = 0;
            q1 = request.POST.get(f'question1_{student.student_id}')
            if q1:
                q1 = (float(q1))
                count += 1
            else:
                q1 = 0
            q2 = request.POST.get(f'question2_{student.student_id}')
            if q2:
                q2 = (float(q2))
                count += 1
            else:
                q2 = 0
            q3 = request.POST.get(f'question3_{student.student_id}')
            if q3:
                q3 = (float(q3))
                count += 1
            else:
                q3 = 0
            q4 = request.POST.get(f'question4_{student.student_id}')
            if q4:
                q4 = (float(q4))
                count += 1
            else:
                q4 = 0
            q5 = request.POST.get(f'question5_{student.student_id}')
            if q5:
                q5 = (float(q5))
                count += 1
            else:
                q5 = 0
            q6 = request.POST.get(f'question6_{student.student_id}')
            if q6:
                q6 = (float(q6))
                count += 1
            else:
                q6 = 0
            q7 = request.POST.get(f'question7_{student.student_id}')
            if q7:
                q7 = (float(q7))
                count += 1
            else:
                q7 = 0
            q8 = request.POST.get(f'question8_{student.student_id}')
            if q8:
                q8 = (float(q8))
                count += 1
            else:
                q8 = 0
            q9 = request.POST.get(f'question9_{student.student_id}')
            if q9:
                q9 = (float(q9))
                count += 1
            else:
                q9 = 0
            if count > 7:
                messages.warning(request, 'A student can not answer more than seven question')
                return HttpResponseRedirect(f'/faculty/Theory_mark_sheet/{course_code}/')
            total_marks = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9
            remark = Teacher_Student_Info.objects.get(student_id = student.student_id, course_code= course_code)
            data = Theory_Marks(
                student_id = student.student_id,
                student_name = student.student_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                course_name = course.course_name,
                course_teacher = course.course_teacher,
                credit = course.credit,
                remarks = remark.remarks,
                q1 = q1,
                q2 = q2,
                q3 = q3,
                q4 = q4,
                q5 = q5,
                q6 = q6,
                q7 = q7,
                q8 = q8,
                q9 = q9,
                total_marks = total_marks,
            )
            checker = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course.course_code)
            flag = False
            for c in checker:
                id = c.id
                flag = True
            if flag == True:
                update_data = Theory_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.student_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    course_name = course.course_name,
                    course_teacher = course.course_teacher,
                    credit = course.credit,
                    remarks = remark.remarks,
                    q1 = q1,
                    q2 = q2,
                    q3 = q3,
                    q4 = q4,
                    q5 = q5,
                    q6 = q6,
                    q7 = q7,
                    q8 = q8,
                    q9 = q9,
                    total_marks = total_marks,
                )
                update_data.save()
            else:
                data.save()
        
        messages.success(request, 'Theory Marks added/updated successfully')
        return HttpResponseRedirect(f'/faculty/show_theory_marks/{course_code}/')
    context = {
        'course_code': course_code,
        'course_name': course.course_name,
        'credit': course.credit,
        'semester_no': course.semister_no,
        'course_teacher': course.course_teacher,
        'regular_students_theory_marks': regular_students_theory_marks,
        'backLogStudents': backLogStudents,
        'special_students_theory_marks': special_students_theory_marks,
    }
    return render(request, 'faculty/update_theory_marks.html', context)

def consolidated_marks_sheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    consolidated_marks_regular = {}
    consolidated_marks_backLog = {}
    consolidated_marks_special = {}
    for student in regular_students:
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        theory_marks = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course_code)
        ct_marks = 0
        attendence_mark = 0
        theory_mark = 0
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        for mark in theory_marks:
            theory_mark = mark.total_marks
        total_marks = ct_marks + attendence_mark + theory_mark
        if total_marks >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks > 74 and total_marks < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks > 69 and total_marks < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks > 64 and total_marks < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks > 59 and total_marks < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks > 54 and total_marks < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks > 49 and total_marks < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks > 44 and total_marks < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks > 39 and total_marks < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        consolidated_marks_regular[student] = {'ct_mark': ct_marks, 'attendence_mark': attendence_mark,
        'theory_mark':theory_mark, 'full_marks': total_marks, 'LG': LG, 'GP': GP}
    
    for student in backLog_students:
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        theory_marks = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course_code)
        ct_marks = 0
        attendence_mark = 0
        theory_mark =0 
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        for mark in theory_marks:
            theory_mark = mark.total_marks
        total_marks = ct_marks + attendence_mark + theory_mark
        if total_marks >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks > 74 and total_marks < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks > 69 and total_marks < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks > 64 and total_marks < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks > 59 and total_marks < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks > 54 and total_marks < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks > 49 and total_marks < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks > 44 and total_marks < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks > 39 and total_marks < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        count += 1
        consolidated_marks_backLog[student] = {'ct_mark': ct_marks, 'attendence_mark': attendence_mark,
        'theory_mark':theory_mark, 'full_marks': total_marks, 'LG': LG, 'GP': GP, 'count': count}
    
    for student in special_students:
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        theory_marks = Theory_Marks.objects.filter(student_id = student.student_id, course_code = course_code)
        ct_marks = 0
        attendence_mark = 0
        theory_mark = 0
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        for mark in theory_marks:
            theory_mark = mark.total_marks
        total_marks = ct_marks + attendence_mark + theory_mark
        if total_marks >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks > 74 and total_marks < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks > 69 and total_marks < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks > 64 and total_marks < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks > 59 and total_marks < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks > 54 and total_marks < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks > 49 and total_marks < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks > 44 and total_marks < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks > 39 and total_marks < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        consolidated_marks_special[student] = {'ct_mark': ct_marks, 'attendence_mark': attendence_mark,
        'theory_mark':theory_mark, 'full_marks': total_marks, 'LG': LG, 'GP': GP}
    
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'consolidated_marks_regular': consolidated_marks_regular,
        'consolidated_marks_backLog': consolidated_marks_backLog,
        'consolidated_marks_special': consolidated_marks_special,
    }
    return render(request, 'faculty/consolidated_marks_sheet.html', context)

def send_to_controller_theory_marks(request,course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Theory_Marks.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Theory_Marks.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Theory_Marks.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'regular_students': regular_students,
        'backLog_students': backLog_students,
        'special_students': special_students,
    }
    return render(request, 'faculty/send_to_controller.html', context)

def lab_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
   
    count = 0
    backLogStudents = {}
    regularStudents = {}
    specialStudents = {}
    submit_button = False
    for stu in regular_students:
        submit_button = True
        student_details = {}
        lab_marks = Lab_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        lab_attendence = 0
        lab_report = 0
        lab_quize = 0
        for c in lab_marks:
            lab_attendence = c.lab_attendence
            lab_report = c.lab_report
            lab_quize = c.lab_quize
        student_details['lab_attendence'] = lab_attendence
        student_details['lab_report'] = lab_report
        student_details['lab_quize'] = lab_quize
        regularStudents[stu] = student_details
        count += 1
    for stu in backLog_students:
        count += 1
        submit_button = True
        student_details = {}
        lab_marks = Lab_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        lab_attendence = 0
        lab_report = 0
        lab_quize = 0
        for c in lab_marks:
            lab_attendence = c.lab_attendence
            lab_report = c.lab_report
            lab_quize = c.lab_quize
        student_details['lab_attendence'] = lab_attendence
        student_details['lab_report'] = lab_report
        student_details['lab_quize'] = lab_quize
        student_details['count'] = count
        backLogStudents[stu] = student_details
    for stu in special_students:
        count += 1
        submit_button = True
        student_details = {}
        lab_marks = Lab_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        lab_attendence = 0
        lab_report = 0
        lab_quize = 0
        for c in lab_marks:
            lab_attendence = c.lab_attendence
            lab_report = c.lab_report
            lab_quize = c.lab_quize
        student_details['lab_attendence'] = lab_attendence
        student_details['lab_report'] = lab_report
        student_details['lab_quize'] = lab_quize
        student_details['count'] = count
        specialStudents[stu] = student_details
    if request.method == 'POST':
        for stu in regular_students:

            lab_attendence = request.POST.get(f'lab_attendence_{stu.student_id}')
            
            if lab_attendence:
                lab_attendence_mark = (float(lab_attendence))
            else:
                lab_attendence_mark = 0
            
            lab_report = request.POST.get(f'lab_report_{stu.student_id}')
            if lab_report:
                lab_report_mark = (float(lab_report))
            else:
                lab_report_mark = 0

            lab_quize = request.POST.get(f'lab_quize_{stu.student_id}')
            if lab_quize:
                lab_quize_mark = (float(lab_quize))
            else:
                lab_quize_mark = 0
            lab_total_mark = lab_attendence_mark + lab_report_mark + lab_quize_mark
            print(lab_attendence_mark, lab_report_mark, lab_quize_mark, lab_total_mark)
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                lab_attendence = lab_attendence_mark,
                lab_report = lab_report_mark,
                lab_quize = lab_quize_mark,
                lab_total_mark = lab_total_mark,
            )
            checker = Lab_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    lab_attendence = lab_attendence_mark,
                    lab_report = lab_report_mark,
                    lab_quize = lab_quize_mark,
                    lab_total_mark = lab_total_mark,
                )
                data.save()
            else:
                data.save()
        for stu in backLog_students:

            lab_attendence = request.POST.get(f'lab_attendence_{stu.student_id}')
            
            if lab_attendence:
                lab_attendence_mark = (float(lab_attendence))
            else:
                lab_attendence_mark = 0
            
            lab_report = request.POST.get(f'lab_report_{stu.student_id}')
            if lab_report:
                lab_report_mark = (float(lab_report))
            else:
                lab_report_mark = 0

            lab_quize = request.POST.get(f'lab_quize_{stu.student_id}')
            if lab_quize:
                lab_quize_mark = (float(lab_quize))
            else:
                lab_quize_mark = 0
            lab_total_mark = lab_attendence_mark + lab_report_mark + lab_quize_mark
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                lab_attendence = lab_attendence_mark,
                lab_report = lab_report_mark,
                lab_quize = lab_quize_mark,
                lab_total_mark = lab_total_mark,
            )
            checker = Lab_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    lab_attendence = lab_attendence_mark,
                    lab_report = lab_report_mark,
                    lab_quize = lab_quize_mark,
                    lab_total_mark = lab_total_mark,
                )
                data.save()
            else:
                data.save()
        for stu in special_students:

            lab_attendence = request.POST.get(f'lab_attendence_{stu.student_id}')
            
            if lab_attendence:
                lab_attendence_mark = (float(lab_attendence))
            else:
                lab_attendence_mark = 0
            
            lab_report = request.POST.get(f'lab_report_{stu.student_id}')
            if lab_report:
                lab_report_mark = (float(lab_report))
            else:
                lab_report_mark = 0

            lab_quize = request.POST.get(f'lab_quize_{stu.student_id}')
            if lab_quize:
                lab_quize_mark = (float(lab_quize))
            else:
                lab_quize_mark = 0
            lab_total_mark = lab_attendence_mark + lab_report_mark + lab_quize_mark
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                lab_attendence = lab_attendence_mark,
                lab_report = lab_report_mark,
                lab_quize = lab_quize_mark,
                lab_total_mark = lab_total_mark,
            )
            checker = Lab_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    lab_attendence = lab_attendence_mark,
                    lab_report = lab_report_mark,
                    lab_quize = lab_quize_mark,
                    lab_total_mark = lab_total_mark,
                )
                data.save()
            else:
                data.save()

        return HttpResponseRedirect(f'/faculty/show_lab_marks/{course_code}/')


    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regularStudents': regularStudents,
        'backLogStudents': backLogStudents,
        'submit_button': submit_button,
        'specialStudents': specialStudents,
    }
    return render(request, 'faculty/lab_marks.html', context)

def final_50_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    regularStudents = {}
    specialStudents = {}
    submit_button = False
    for stu in regular_students:
        submit_button = True
        student_details = {}
        lab_final_50_marks = Lab_Final_50_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        final_practical_exam = 0
        viva_voce = 0
        for c in lab_final_50_marks:
            final_practical_exam = c.final_practical_exam
            viva_voce = c.viva_voce
        student_details['final_practical_exam'] = final_practical_exam
        student_details['viva_voce'] = viva_voce
        regularStudents[stu] = student_details
        count += 1
    for stu in backLog_students:
        count += 1
        submit_button = True
        student_details = {}
        lab_final_50_marks = Lab_Final_50_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        final_practical_exam = 0
        viva_voce = 0
        for c in lab_final_50_marks:
            final_practical_exam = c.final_practical_exam
            viva_voce = c.viva_voce
        student_details['final_practical_exam'] = final_practical_exam
        student_details['viva_voce'] = viva_voce
        student_details['count'] = count
        backLogStudents[stu] = student_details
    for stu in special_students:
        count += 1
        submit_button = True
        student_details = {}
        lab_final_50_marks = Lab_Final_50_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        final_practical_exam = 0
        viva_voce = 0
        for c in lab_final_50_marks:
            final_practical_exam = c.final_practical_exam
            viva_voce = c.viva_voce
        student_details['final_practical_exam'] = final_practical_exam
        student_details['viva_voce'] = viva_voce
        student_details['count'] = count
        specialStudents[stu] = student_details
    if request.method == 'POST':
        for stu in regular_students:
            final_practical_exam = request.POST.get(f'final_practical_exam_{stu.student_id}')
            if final_practical_exam:
                final_practical_exam = float(final_practical_exam)
            else:
                final_practical_exam = 0
            
            viva_voce = request.POST.get(f'viva_voce_{stu.student_id}')
            if viva_voce:
                viva_voce = float(viva_voce)
            else:
                viva_voce = 0
            total_mark = final_practical_exam + viva_voce
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Final_50_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                final_practical_exam = final_practical_exam,
                viva_voce = viva_voce,
                total_mark = total_mark,
            )
            checker = Lab_Final_50_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Final_50_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    final_practical_exam = final_practical_exam,
                    viva_voce = viva_voce,
                    total_mark = total_mark,
                )
                data.save()
            else:
                data.save()
        for stu in backLog_students:
            final_practical_exam = request.POST.get(f'final_practical_exam_{stu.student_id}')
            if final_practical_exam:
                final_practical_exam = float(final_practical_exam)
            else:
                final_practical_exam = 0
            
            viva_voce = request.POST.get(f'viva_voce_{stu.student_id}')
            if viva_voce:
                viva_voce = float(viva_voce)
            else:
                viva_voce = 0
            total_mark = final_practical_exam + viva_voce
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Final_50_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                final_practical_exam = final_practical_exam,
                viva_voce = viva_voce,
                total_mark = total_mark,
            )
            checker = Lab_Final_50_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Final_50_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    final_practical_exam = final_practical_exam,
                    viva_voce = viva_voce,
                    total_mark = total_mark,
                )
                data.save()
            else:
                data.save()
        for stu in special_students:
            final_practical_exam = request.POST.get(f'final_practical_exam_{stu.student_id}')
            if final_practical_exam:
                final_practical_exam = float(final_practical_exam)
            else:
                final_practical_exam = 0
            
            viva_voce = request.POST.get(f'viva_voce_{stu.student_id}')
            if viva_voce:
                viva_voce = float(viva_voce)
            else:
                viva_voce = 0
            total_mark = final_practical_exam + viva_voce
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Final_50_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                final_practical_exam = final_practical_exam,
                viva_voce = viva_voce,
                total_mark = total_mark,
            )
            checker = Lab_Final_50_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Final_50_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    final_practical_exam = final_practical_exam,
                    viva_voce = viva_voce,
                    total_mark = total_mark,
                )
                data.save()
            else:
                data.save()
        return HttpResponseRedirect(f'/faculty/show_final_50_marks/{course_code}/')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regularStudents': regularStudents,
        'backLogStudents': backLogStudents,
        'submit_button': submit_button,
        'specialStudents': specialStudents,
    }
    return render(request, 'faculty/final_50_marks.html', context)

def consoilated_lab_marksheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    submit_button = False
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        final_practical_exam_checker = Lab_Final_50_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        final_practical_exam_mark = 0
        for c in final_practical_exam_checker:
            final_practical_exam_mark = c.total_mark
        labreport_attendence_quize_checker = Lab_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        labreport_attendence_quize_mark = 0
        for c in labreport_attendence_quize_checker:
            labreport_attendence_quize_mark = c.lab_total_mark
        total_marks_100 = final_practical_exam_mark + labreport_attendence_quize_mark
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'final_practical_exam_mark': final_practical_exam_mark, 'labreport_attendence_quize_mark': labreport_attendence_quize_mark,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
        submit_button = True
        data = Final_MarkSheet_Lab_Course(
            student_id = student.student_id,
            student_name = student.first_name + " " + student.last_name,
            session = student.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = stu.remarks,
            hall = student.hall,
            final_practical_exam_mark = final_practical_exam_mark,
            labreport_attendence_quize_mark = labreport_attendence_quize_mark,
            total_marks = total_marks_100,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Lab_Course.objects.filter(student_id = student.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Lab_Course(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    credits = course.credit,
                    remarks = stu.remarks,
                    hall = student.hall,
                    final_practical_exam_mark = final_practical_exam_mark,
                    labreport_attendence_quize_mark = labreport_attendence_quize_mark,
                    total_marks = total_marks_100,
                    GP = GP,
                    PS = PS,
                    LG = LG,
                )
            data.save()
        else:
            data.save()
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        final_practical_exam_checker = Lab_Final_50_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        final_practical_exam_mark = 0
        for c in final_practical_exam_checker:
            final_practical_exam_mark = c.total_mark
        labreport_attendence_quize_checker = Lab_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        labreport_attendence_quize_mark = 0
        for c in labreport_attendence_quize_checker:
            labreport_attendence_quize_mark = c.lab_total_mark
        total_marks_100 = final_practical_exam_mark + labreport_attendence_quize_mark
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'final_practical_exam_mark': final_practical_exam_mark, 'labreport_attendence_quize_mark': labreport_attendence_quize_mark,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
        submit_button = True
        data = Final_MarkSheet_Lab_Course(
            student_id = student.student_id,
            student_name = student.first_name + " " + student.last_name,
            session = student.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = stu.remarks,
            hall = student.hall,
            final_practical_exam_mark = final_practical_exam_mark,
            labreport_attendence_quize_mark = labreport_attendence_quize_mark,
            total_marks = total_marks_100,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Lab_Course.objects.filter(student_id = student.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Lab_Course(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    credits = course.credit,
                    remarks = stu.remarks,
                    hall = student.hall,
                    final_practical_exam_mark = final_practical_exam_mark,
                    labreport_attendence_quize_mark = labreport_attendence_quize_mark,
                    total_marks = total_marks_100,
                    GP = GP,
                    PS = PS,
                    LG = LG,
                )
            data.save()
        else:
            data.save()
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        final_practical_exam_checker = Lab_Final_50_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        final_practical_exam_mark = 0
        for c in final_practical_exam_checker:
            final_practical_exam_mark = c.total_mark
        labreport_attendence_quize_checker = Lab_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        labreport_attendence_quize_mark = 0
        for c in labreport_attendence_quize_checker:
            labreport_attendence_quize_mark = c.lab_total_mark
        total_marks_100 = final_practical_exam_mark + labreport_attendence_quize_mark
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'final_practical_exam_mark': final_practical_exam_mark, 'labreport_attendence_quize_mark': labreport_attendence_quize_mark,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
        submit_button = True
        data = Final_MarkSheet_Lab_Course(
            student_id = student.student_id,
            student_name = student.first_name + " " + student.last_name,
            session = student.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = stu.remarks,
            hall = student.hall,
            final_practical_exam_mark = final_practical_exam_mark,
            labreport_attendence_quize_mark = labreport_attendence_quize_mark,
            total_marks = total_marks_100,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Lab_Course.objects.filter(student_id = student.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Lab_Course(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    credits = course.credit,
                    remarks = stu.remarks,
                    hall = student.hall,
                    final_practical_exam_mark = final_practical_exam_mark,
                    labreport_attendence_quize_mark = labreport_attendence_quize_mark,
                    total_marks = total_marks_100,
                    GP = GP,
                    PS = PS,
                    LG = LG,
                )
            data.save()
        else:
            data.save()
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'submit_button': submit_button,
        'special_student': special_student,
    }
    return render(request, 'faculty/consoilated_lab_marksheet.html', context)

def show_lab_marks(requset, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Lab_Marks.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
    backLog_students = Lab_Marks.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
    special_students = Lab_Marks.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'special_student': special_student,
    }
    return render(requset, 'faculty/show_lab_marks.html', context)

def edit_lab_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Lab_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Lab_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Lab_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    submit_button = False
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    if request.method == 'POST':
        for stu in regular_students:

            lab_attendence = request.POST.get(f'lab_attendence_{stu.student_id}')
            
            if lab_attendence:
                lab_attendence_mark = (float(lab_attendence))
            else:
                lab_attendence_mark = 0
            
            lab_report = request.POST.get(f'lab_report_{stu.student_id}')
            if lab_report:
                lab_report_mark = (float(lab_report))
            else:
                lab_report_mark = 0

            lab_quize = request.POST.get(f'lab_quize_{stu.student_id}')
            if lab_quize:
                lab_quize_mark = (float(lab_quize))
            else:
                lab_quize_mark = 0
            lab_total_mark = lab_attendence_mark + lab_report_mark + lab_quize_mark
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                lab_attendence = lab_attendence_mark,
                lab_report = lab_report_mark,
                lab_quize = lab_quize_mark,
                lab_total_mark = lab_total_mark,
            )
            checker = Lab_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    lab_attendence = lab_attendence_mark,
                    lab_report = lab_report_mark,
                    lab_quize = lab_quize_mark,
                    lab_total_mark = lab_total_mark,
                )
                data.save()
            else:
                data.save()
        for stu in backLog_students:

            lab_attendence = request.POST.get(f'lab_attendence_{stu.student_id}')
            
            if lab_attendence:
                lab_attendence_mark = (float(lab_attendence))
            else:
                lab_attendence_mark = 0
            
            lab_report = request.POST.get(f'lab_report_{stu.student_id}')
            if lab_report:
                lab_report_mark = (float(lab_report))
            else:
                lab_report_mark = 0

            lab_quize = request.POST.get(f'lab_quize_{stu.student_id}')
            if lab_quize:
                lab_quize_mark = (float(lab_quize))
            else:
                lab_quize_mark = 0
            lab_total_mark = lab_attendence_mark + lab_report_mark + lab_quize_mark
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                lab_attendence = lab_attendence_mark,
                lab_report = lab_report_mark,
                lab_quize = lab_quize_mark,
                lab_total_mark = lab_total_mark,
            )
            checker = Lab_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    lab_attendence = lab_attendence_mark,
                    lab_report = lab_report_mark,
                    lab_quize = lab_quize_mark,
                    lab_total_mark = lab_total_mark,
                )
                data.save()
            else:
                data.save()
        for stu in special_students:

            lab_attendence = request.POST.get(f'lab_attendence_{stu.student_id}')
            
            if lab_attendence:
                lab_attendence_mark = (float(lab_attendence))
            else:
                lab_attendence_mark = 0
            
            lab_report = request.POST.get(f'lab_report_{stu.student_id}')
            if lab_report:
                lab_report_mark = (float(lab_report))
            else:
                lab_report_mark = 0

            lab_quize = request.POST.get(f'lab_quize_{stu.student_id}')
            if lab_quize:
                lab_quize_mark = (float(lab_quize))
            else:
                lab_quize_mark = 0
            lab_total_mark = lab_attendence_mark + lab_report_mark + lab_quize_mark
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                lab_attendence = lab_attendence_mark,
                lab_report = lab_report_mark,
                lab_quize = lab_quize_mark,
                lab_total_mark = lab_total_mark,
            )
            checker = Lab_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    lab_attendence = lab_attendence_mark,
                    lab_report = lab_report_mark,
                    lab_quize = lab_quize_mark,
                    lab_total_mark = lab_total_mark,
                )
                data.save()
            else:
                data.save()

        return HttpResponseRedirect(f'/faculty/show_lab_marks/{course_code}/')


    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'submit_button': submit_button,
        'special_student': special_student,
    }
    return render(request, 'faculty/edit_lab_marks.html', context)

def show_final_50_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Lab_Final_50_Marks.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
    backLog_students = Lab_Final_50_Marks.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
    special_students = Lab_Final_50_Marks.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'special_student': special_student,
    }
    return render(request, 'faculty/show_final_50_marks.html', context)

def edit_lab_final_50_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Lab_Final_50_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Lab_Final_50_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Lab_Final_50_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    submit_button = False
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    if request.method == 'POST':
        for stu in regular_students:
            final_practical_exam = request.POST.get(f'final_practical_exam_{stu.student_id}')
            if final_practical_exam:
                final_practical_exam = float(final_practical_exam)
            else:
                final_practical_exam = 0
            
            viva_voce = request.POST.get(f'viva_voce_{stu.student_id}')
            if viva_voce:
                viva_voce = float(viva_voce)
            else:
                viva_voce = 0
            total_mark = final_practical_exam + viva_voce
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Final_50_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                final_practical_exam = final_practical_exam,
                viva_voce = viva_voce,
                total_mark = total_mark,
            )
            checker = Lab_Final_50_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Final_50_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    final_practical_exam = final_practical_exam,
                    viva_voce = viva_voce,
                    total_mark = total_mark,
                )
                data.save()
            else:
                data.save()
        for stu in backLog_students:
            final_practical_exam = request.POST.get(f'final_practical_exam_{stu.student_id}')
            if final_practical_exam:
                final_practical_exam = float(final_practical_exam)
            else:
                final_practical_exam = 0
            
            viva_voce = request.POST.get(f'viva_voce_{stu.student_id}')
            if viva_voce:
                viva_voce = float(viva_voce)
            else:
                viva_voce = 0
            total_mark = final_practical_exam + viva_voce
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Final_50_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                final_practical_exam = final_practical_exam,
                viva_voce = viva_voce,
                total_mark = total_mark,
            )
            checker = Lab_Final_50_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Final_50_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    final_practical_exam = final_practical_exam,
                    viva_voce = viva_voce,
                    total_mark = total_mark,
                )
                data.save()
            else:
                data.save()
        for stu in special_students:
            final_practical_exam = request.POST.get(f'final_practical_exam_{stu.student_id}')
            if final_practical_exam:
                final_practical_exam = float(final_practical_exam)
            else:
                final_practical_exam = 0
            
            viva_voce = request.POST.get(f'viva_voce_{stu.student_id}')
            if viva_voce:
                viva_voce = float(viva_voce)
            else:
                viva_voce = 0
            total_mark = final_practical_exam + viva_voce
            student = Student.objects.get(student_id= stu.student_id)
            data = Lab_Final_50_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                final_practical_exam = final_practical_exam,
                viva_voce = viva_voce,
                total_mark = total_mark,
            )
            checker = Lab_Final_50_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Lab_Final_50_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    final_practical_exam = final_practical_exam,
                    viva_voce = viva_voce,
                    total_mark = total_mark,
                )
                data.save()
            else:
                data.save()
        return HttpResponseRedirect(f'/faculty/show_final_50_marks/{course_code}/')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'submit_button': submit_button,
        'special_student': special_student,
    }
    return render(request, 'faculty/edit_lab_final_50_marks.html', context)

def project_course_details(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    for stu in backLog_students:
        count += 1
        backLogStudents[stu] = count
    context = {
    'c_code' : (course.course_code),
    'c_name' : (course.course_name),
    'c_credit' : (course.credit),
    'c_teacher' : course.course_teacher,
    'regular_students': regular_students,
    'backLogStudents': backLogStudents,
    'special_students': special_students,
    }
    return render(request, 'faculty/project_course_details.html', context)

def project_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    regularStudents = {}
    specialStudents = {}
    submit_button = False
    for stu in regular_students:
        submit_button = True
        student_details = {}
        project_marks = Project_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        supervisor_marks = 0
        defence_marks = 0
        for c in project_marks:
            supervisor_marks = c.supervisor_marks
            defence_marks = c.defence_marks
        student_details['supervisor_marks'] = supervisor_marks
        student_details['defence_marks'] = defence_marks
        regularStudents[stu] = student_details
        count += 1
    for stu in backLog_students:
        count += 1
        submit_button = True
        student_details = {}
        project_marks = Project_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        supervisor_marks = 0
        defence_marks = 0
        for c in project_marks:
            supervisor_marks = c.supervisor_marks
            defence_marks = c.defence_marks
        student_details['supervisor_marks'] = supervisor_marks
        student_details['defence_marks'] = defence_marks
        student_details['count'] = count
        backLogStudents[stu] = student_details
    for stu in special_students:
        count += 1
        submit_button = True
        student_details = {}
        project_marks = Project_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        supervisor_marks = 0
        defence_marks = 0
        for c in project_marks:
            supervisor_marks = c.supervisor_marks
            defence_marks = c.defence_marks
        student_details['supervisor_marks'] = supervisor_marks
        student_details['defence_marks'] = defence_marks
        student_details['count'] = count
        specialStudents[stu] = student_details
    if request.method == 'POST':
        for stu in regular_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in backLog_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in special_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        return HttpResponseRedirect(f'/faculty/show_project_marks/{course_code}')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regularStudents': regularStudents,
        'backLogStudents': backLogStudents,
        'submit_button': submit_button,
        'specialStudents': specialStudents,
    }
    return render(request, 'faculty/project_marks.html', context)

def viva_course_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')

    count = 0
    backLogStudents = {}
    regularStudents = {}
    specialStudents = {}
    submit_button = False
    for stu in regular_students:
        submit_button = True
        student_details = {}
        project_marks = Viva_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        total_mark = 0
        for c in project_marks:
            total_mark = c.total_mark
        student_details['total_mark'] = total_mark
        regularStudents[stu] = student_details
        count += 1
    for stu in backLog_students:
        count += 1
        submit_button = True
        student_details = {}
        project_marks = Viva_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        total_mark = 0
        for c in project_marks:
            total_mark = c.total_mark
        student_details['total_mark'] = total_mark
        student_details['count'] = count
        backLogStudents[stu] = student_details
    for stu in special_students:
        count += 1
        submit_button = True
        student_details = {}
        project_marks = Viva_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        total_mark = 0
        for c in project_marks:
            total_mark = c.total_mark
        student_details['total_mark'] = total_mark
        student_details['count'] = count
        specialStudents[stu] = student_details
    if request.method == 'POST':
        for stu in regular_students:
            viva_marks = request.POST.get(f'viva_marks_{stu.student_id}')
            if viva_marks:
                viva_marks_100 = float(viva_marks)
            else:
                viva_marks_100 = 0
            
            total_marks_100 = viva_marks_100

            student = Student.objects.get(student_id= stu.student_id)
            data = Viva_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                total_mark = total_marks_100,
            )
            checker = Viva_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Viva_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in backLog_students:
            viva_marks = request.POST.get(f'viva_marks_{stu.student_id}')
            if viva_marks:
                viva_marks_100 = float(viva_marks)
            else:
                viva_marks_100 = 0
            
            total_marks_100 = viva_marks_100

            student = Student.objects.get(student_id= stu.student_id)
            data = Viva_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                total_mark = total_marks_100,
            )
            checker = Viva_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Viva_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in special_students:
            viva_marks = request.POST.get(f'viva_marks_{stu.student_id}')
            if viva_marks:
                viva_marks_100 = float(viva_marks)
            else:
                viva_marks_100 = 0
            
            total_marks_100 = viva_marks_100

            student = Student.objects.get(student_id= stu.student_id)
            data = Viva_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                total_mark = total_marks_100,
            )
            checker = Viva_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Viva_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        return HttpResponseRedirect(f'/faculty/show_viva_marks/{course_code}')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regularStudents': regularStudents,
        'backLogStudents': backLogStudents,
        'submit_button': submit_button,
        'specialStudents': specialStudents,
    }
    return render(request, 'faculty/viva_course_marks.html', context)

def research_project_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
   
    count = 0
    backLogStudents = {}
    regularStudents = {}
    specialStudents = {}
    submit_button = False
    for stu in regular_students:
        submit_button = True
        student_details = {}
        project_marks = Research_Project_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        supervisor_marks = 0
        defence_marks = 0
        for c in project_marks:
            supervisor_marks = c.supervisor_marks
            defence_marks = c.defence_marks
        student_details['supervisor_marks'] = supervisor_marks
        student_details['defence_marks'] = defence_marks
        regularStudents[stu] = student_details
        count += 1
    for stu in backLog_students:
        count += 1
        submit_button = True
        student_details = {}
        project_marks = Research_Project_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        supervisor_marks = 0
        defence_marks = 0
        for c in project_marks:
            supervisor_marks = c.supervisor_marks
            defence_marks = c.defence_marks
        student_details['supervisor_marks'] = supervisor_marks
        student_details['defence_marks'] = defence_marks
        student_details['count'] = count
        backLogStudents[stu] = student_details
    for stu in special_students:
        count += 1
        submit_button = True
        student_details = {}
        project_marks = Research_Project_Marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        supervisor_marks = 0
        defence_marks = 0
        for c in project_marks:
            supervisor_marks = c.supervisor_marks
            defence_marks = c.defence_marks
        student_details['supervisor_marks'] = supervisor_marks
        student_details['defence_marks'] = defence_marks
        student_details['count'] = count
        specialStudents[stu] = student_details
    if request.method == 'POST':
        for stu in regular_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Research_Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Research_Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in backLog_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Research_Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Research_Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in special_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Research_Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Research_Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        return HttpResponseRedirect(f'/faculty/show_research_project_marks/{course_code}')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regularStudents': regularStudents,
        'backLogStudents': backLogStudents,
        'submit_button': submit_button,
        'specialStudents': specialStudents,
    }
    return render(request, 'faculty/research_project_marks.html', context)

def show_project_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Project_Marks.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
    backLog_students = Project_Marks.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
    special_students = Project_Marks.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'special_student': special_student,
    }
    return render(request, 'faculty/show_project_marks.html', context)

def show_viva_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Viva_Marks.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
    backLog_students = Viva_Marks.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
    special_students = Viva_Marks.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'special_student': special_student,
    }
    return render(request, 'faculty/show_viva_marks.html', context)

def show_research_project_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Research_Project_Marks.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
    backLog_students = Research_Project_Marks.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
    special_students = Research_Project_Marks.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'special_student': special_student,
    }
    return render(request, 'faculty/show_research_project_marks.html', context)

def edit_project_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Project_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Project_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Project_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    regular_student = {}
    backlog_student = {}
    special_student = {}
    submit_button = False
    count = 0
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    if request.method == 'POST':
        for stu in regular_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in backLog_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in special_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        return HttpResponseRedirect(f'/faculty/show_project_marks/{course_code}')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'submit_button': submit_button,
        'special_student': special_student,
    }
    return render(request, 'faculty/edit_project_marks.html', context)

def edit_viva_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Viva_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Viva_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Viva_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    regular_student = {}
    backlog_student = {}
    special_student = {}
    submit_button = False
    count = 0
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    if request.method == 'POST':
        for stu in regular_students:
            viva_marks = request.POST.get(f'viva_marks_{stu.student_id}')
            if viva_marks:
                viva_marks_100 = float(viva_marks)
            else:
                viva_marks_100 = 0
            
            total_marks_100 = viva_marks_100

            student = Student.objects.get(student_id= stu.student_id)
            data = Viva_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                total_mark = total_marks_100,
            )
            checker = Viva_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Viva_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in backLog_students:
            viva_marks = request.POST.get(f'viva_marks_{stu.student_id}')
            if viva_marks:
                viva_marks_100 = float(viva_marks)
            else:
                viva_marks_100 = 0
            
            total_marks_100 = viva_marks_100

            student = Student.objects.get(student_id= stu.student_id)
            data = Viva_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                total_mark = total_marks_100,
            )
            checker = Viva_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Viva_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in special_students:
            viva_marks = request.POST.get(f'viva_marks_{stu.student_id}')
            if viva_marks:
                viva_marks_100 = float(viva_marks)
            else:
                viva_marks_100 = 0
            
            total_marks_100 = viva_marks_100

            student = Student.objects.get(student_id= stu.student_id)
            data = Viva_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                total_mark = total_marks_100,
            )
            checker = Viva_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Viva_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        return HttpResponseRedirect(f'/faculty/show_viva_marks/{course_code}')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'submit_button': submit_button,
        'special_student': special_student,
    }
    return render(request, 'faculty/edit_viva_marks.html', context)

def edit_research_project_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Research_Project_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Research_Project_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Research_Project_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    regular_student = {}
    backlog_student = {}
    special_student = {}
    submit_button = False
    count = 0
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'count': count}
        submit_button = True
    if request.method == 'POST':
        for stu in regular_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Research_Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Research_Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in backLog_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Research_Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Research_Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        for stu in special_students:
            supervisor_marks = request.POST.get(f'supervisor_marks_{stu.student_id}')
            if supervisor_marks:
                supervisor_marks_70 = float(supervisor_marks)
            else:
                supervisor_marks_70 = 0
            
            defence_marks = request.POST.get(f'defence_marks_{stu.student_id}')
            if defence_marks:
                defence_marks_30 = float(defence_marks)
            else:
                defence_marks_30 = 0
            total_marks_100 = supervisor_marks_70 + defence_marks_30

            student = Student.objects.get(student_id= stu.student_id)
            data = Research_Project_Marks(
                student_id = student.student_id,
                student_name = student.first_name + " " + student.last_name,
                session = student.session,
                semester_no = course.semister_no,
                course_code = course_code,
                course_name = course.course_name,
                credit = course.credit,
                remarks = stu.remarks,
                supervisor_marks = supervisor_marks_70,
                defence_marks = defence_marks_30,
                total_mark = total_marks_100,
            )
            checker = Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = Research_Project_Marks(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course_code,
                    course_name = course.course_name,
                    credit = course.credit,
                    remarks = stu.remarks,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_mark = total_marks_100,
                )
                data.save()
            else:
                data.save()
        return HttpResponseRedirect(f'/faculty/show_research_project_marks/{course_code}')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'submit_button': submit_button,
        'special_student': special_student,
    }
    return render(request, 'faculty/edit_research_project_marks.html', context)

def consoilated_project_marksheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Project_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Project_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Project_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    submit_button = False
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        project_marks_checker = Project_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        total_marks_100 = 0
        for c in project_marks_checker:
            total_marks_100 = c.total_mark
            supervisor_marks_70 = c.supervisor_marks
            defence_marks_30 = c.defence_marks
          
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'supervisor_marks_70': supervisor_marks_70, 'defence_marks_30': defence_marks_30,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
        data = Final_MarkSheet_Project_Course(
            student_id = student.student_id,
            student_name = student.first_name + " " + student.last_name,
            session = student.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = stu.remarks,
            hall = student.hall,
            supervisor_marks = supervisor_marks_70,
            defence_marks = defence_marks_30,
            total_marks = total_marks_100,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Project_Course.objects.filter(student_id = student.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Project_Course(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    credits = course.credit,
                    remarks = stu.remarks,
                    hall = student.hall,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_marks = total_marks_100,
                    GP = GP,
                    PS = PS,
                    LG = LG,
                )
            data.save()
        else:
            data.save()
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        project_marks_checker = Project_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        total_marks_100 = 0
        for c in project_marks_checker:
            total_marks_100 = c.total_mark
            supervisor_marks_70 = c.supervisor_marks
            defence_marks_30 = c.defence_marks
          
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'supervisor_marks_70': supervisor_marks_70, 'defence_marks_30': defence_marks_30,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
        data = Final_MarkSheet_Project_Course(
            student_id = student.student_id,
            student_name = student.first_name + " " + student.last_name,
            session = student.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = stu.remarks,
            hall = student.hall,
            supervisor_marks = supervisor_marks_70,
            defence_marks = defence_marks_30,
            total_marks = total_marks_100,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Project_Course.objects.filter(student_id = student.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Project_Course(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    credits = course.credit,
                    remarks = stu.remarks,
                    hall = student.hall,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_marks = total_marks_100,
                    GP = GP,
                    PS = PS,
                    LG = LG,
                )
            data.save()
        else:
            data.save()
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        project_marks_checker = Project_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        total_marks_100 = 0
        for c in project_marks_checker:
            total_marks_100 = c.total_mark
            supervisor_marks_70 = c.supervisor_marks
            defence_marks_30 = c.defence_marks
          
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'supervisor_marks_70': supervisor_marks_70, 'defence_marks_30': defence_marks_30,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
        data = Final_MarkSheet_Project_Course(
            student_id = student.student_id,
            student_name = student.first_name + " " + student.last_name,
            session = student.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = stu.remarks,
            hall = student.hall,
            supervisor_marks = supervisor_marks_70,
            defence_marks = defence_marks_30,
            total_marks = total_marks_100,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Project_Course.objects.filter(student_id = student.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Project_Course(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    credits = course.credit,
                    remarks = stu.remarks,
                    hall = student.hall,
                    supervisor_marks = supervisor_marks_70,
                    defence_marks = defence_marks_30,
                    total_marks = total_marks_100,
                    GP = GP,
                    PS = PS,
                    LG = LG,
                )
            data.save()
        else:
            data.save()
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'special_student': special_student,
    }
    return render(request, 'faculty/consoilated_project_marksheet.html', context)

def consoilated_research_project_marksheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Research_Project_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Research_Project_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Research_Project_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    submit_button = False
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        project_marks_checker = Research_Project_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        total_marks_100 = 0
        for c in project_marks_checker:
            total_marks_100 = c.total_mark
            supervisor_marks_70 = c.supervisor_marks
            defence_marks_30 = c.defence_marks
          
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'supervisor_marks_70': supervisor_marks_70, 'defence_marks_30': defence_marks_30,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        project_marks_checker = Research_Project_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        total_marks_100 = 0
        for c in project_marks_checker:
            total_marks_100 = c.total_mark
            supervisor_marks_70 = c.supervisor_marks
            defence_marks_30 = c.defence_marks
          
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        backlog_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'supervisor_marks_70': supervisor_marks_70, 'defence_marks_30': defence_marks_30,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        project_marks_checker = Research_Project_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        total_marks_100 = 0
        for c in project_marks_checker:
            total_marks_100 = c.total_mark
            supervisor_marks_70 = c.supervisor_marks
            defence_marks_30 = c.defence_marks
          
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        special_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'supervisor_marks_70': supervisor_marks_70, 'defence_marks_30': defence_marks_30,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'special_student': special_student,
    }
    return render(request, 'faculty/consoilated_research_project_marksheet.html', context)

def consoilated_viva_marksheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Viva_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Viva_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Viva_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    count = 0
    regular_student = {}
    backlog_student = {}
    special_student = {}
    for stu in regular_students:
        student = Student.objects.get(student_id= stu.student_id)
        viva_marks_checker = Viva_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        total_marks_100 = 0
        for c in viva_marks_checker:
            total_marks_100 = c.total_mark
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
        data = Final_MarkSheet_Viva_Course(
            student_id = student.student_id,
            student_name = student.first_name + " " + student.last_name,
            session = student.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = stu.remarks,
            hall = student.hall,
            total_marks = total_marks_100,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Viva_Course.objects.filter(student_id = student.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Viva_Course(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    credits = course.credit,
                    remarks = stu.remarks,
                    hall = student.hall,
                    total_marks = total_marks_100,
                    GP = GP,
                    PS = PS,
                    LG = LG,
                )
            data.save()
        else:
            data.save()
    for stu in backLog_students:
        student = Student.objects.get(student_id= stu.student_id)
        viva_marks_checker = Viva_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        total_marks_100 = 0
        for c in viva_marks_checker:
            total_marks_100 = c.total_mark
          
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
        data = Final_MarkSheet_Viva_Course(
            student_id = student.student_id,
            student_name = student.first_name + " " + student.last_name,
            session = student.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = stu.remarks,
            hall = student.hall,
            total_marks = total_marks_100,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Viva_Course.objects.filter(student_id = student.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Viva_Course(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    credits = course.credit,
                    remarks = stu.remarks,
                    hall = student.hall,
                    total_marks = total_marks_100,
                    GP = GP,
                    PS = PS,
                    LG = LG,
                )
            data.save()
        else:
            data.save()
    for stu in special_students:
        student = Student.objects.get(student_id= stu.student_id)
        viva_marks_checker = Viva_Marks.objects.filter(student_id = stu.student_id, course_code= course_code)
        total_marks_100 = 0
        for c in viva_marks_checker:
            total_marks_100 = c.total_mark
          
        if total_marks_100 >= 80:
            LG = 'A+'
            GP = 4.00
        elif (total_marks_100 > 74 and total_marks_100 < 80):
            LG = 'A'
            GP = 3.75
        elif (total_marks_100 > 69 and total_marks_100 < 75):
            LG = 'A-'
            GP = 3.50
        elif (total_marks_100 > 64 and total_marks_100 < 70):
            LG = 'B'
            GP = 3.25
        elif (total_marks_100 > 59 and total_marks_100 < 65):
            LG = 'B'
            GP = 3.00
        elif (total_marks_100 > 54 and total_marks_100 < 60):
            LG = 'B-'
            GP = 2.75
        elif (total_marks_100 > 49 and total_marks_100 < 55):
            LG = 'C+'
            GP = 2.50
        elif (total_marks_100 > 44 and total_marks_100 < 50):
            LG = 'C'
            GP = 2.25
        elif (total_marks_100 > 39 and total_marks_100 < 45):
            LG = 'D'
            GP = 2.00
        else:
            LG = 'F'
            GP = 0.00
        PS = course.credit * GP
        count += 1
        regular_student[stu] = {'full_name': student.first_name + " " + student.last_name,
        'total_marks_100': total_marks_100, 'LG': LG, 'GP': GP, 'PS': PS, 'count': count}
        data = Final_MarkSheet_Viva_Course(
            student_id = student.student_id,
            student_name = student.first_name + " " + student.last_name,
            session = student.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = stu.remarks,
            hall = student.hall,
            total_marks = total_marks_100,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Viva_Course.objects.filter(student_id = student.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Viva_Course(
                    id = id,
                    student_id = student.student_id,
                    student_name = student.first_name + " " + student.last_name,
                    session = student.session,
                    semester_no = course.semister_no,
                    course_code = course.course_code,
                    credits = course.credit,
                    remarks = stu.remarks,
                    hall = student.hall,
                    total_marks = total_marks_100,
                    GP = GP,
                    PS = PS,
                    LG = LG,
                )
            data.save()
        else:
            data.save()
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'regular_student': regular_student,
        'backlog_student': backlog_student,
        'special_student': special_student,
    }
    return render(request, 'faculty/consoilated_viva_marksheet.html', context)

def research_project_course_details(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    for stu in backLog_students:
        count += 1
        backLogStudents[stu] = count
    context = {
    'c_code' : (course.course_code),
    'c_name' : (course.course_name),
    'c_credit' : (course.credit),
    'c_teacher' : course.course_teacher,
    'regular_students': regular_students,
    'backLogStudents': backLogStudents,
    'special_students': special_students,
    }
    return render(request, 'faculty/research_project_course_details.html', context)

def viva_project_course_details(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    for stu in regular_students:
        count += 1
    for stu in backLog_students:
        count += 1
        backLogStudents[stu] = count
    context = {
    'c_code' : (course.course_code),
    'c_name' : (course.course_name),
    'c_credit' : (course.credit),
    'c_teacher' : course.course_teacher,
    'regular_students': regular_students,
    'backLogStudents': backLogStudents,
    'special_students': special_students,
    }
    return render(request, 'faculty/viva_project_course_details.html', context)