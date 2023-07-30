import math
from django.shortcuts import render, HttpResponseRedirect
from authentication.models import ExamCommitte, Student
from chairman.models import Registration_By_Semester, Running_Semester, Course, Teacher_Student_Info
from django.contrib.auth import logout
from faculty.models import *
from . models import Final_MarkSheet_ResearchProject_Course, External_teacher_marks, Third_Examinner_ResearchProject_Marks, Third_Examinner_Marks, External_Teacher_Research_Project_Marks, Final_MarkSheet_Theory_Course
from django.contrib import messages
from examcommite.models import Final_MarkSheet_Theory_Course, Final_MarkSheet_ResearchProject_Course
# Create your views here.
def exam_committe_profile(request):
    exam_committe = ExamCommitte.objects.filter(email = request.user)
    return render(request, 'examcommite/profile.html', {'exam_committe': exam_committe})
#logout
def exam_committe_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')

def exam_committte_current_courses(request):
    exam_committe = ExamCommitte.objects.filter(email = request.user)
    running_semester = Running_Semester.objects.all()
    courses = Course.objects.all()
    context={
        'exam_committe': exam_committe,
        'running_semester': running_semester,
        'courses': courses,
    }
    return render(request, 'examcommite/current_courses.html', context)

def exam_committte_special_courses(request):
    all_semesters = ['1st Year 1st Semester', '1st Year 2nd Semester', '2nd Year 1st Semester', '2nd Year 2nd Semester',
    '3rd Year 1st Semester', '3rd Year 2nd Semester', '4th Year 1st Semester', '4th Year 2nd Semester']
    running_semester = Running_Semester.objects.all()
    exam_committe = ExamCommitte.objects.filter(email = request.user)
    courses = Course.objects.all()
    special_semester = []
    for s in all_semesters:
        flag = False
        for r in running_semester:
            if s == r.semester_no:
                flag = True
        if flag == False:
            special_semester.append(s)
    
    context = {
        'exam_committe': exam_committe,
        'special_semester': special_semester,
        'courses': courses,
    }
    
    return render(request, 'examcommite/special_courses.html', context)

def exam_committe_course_details(request, course_code):
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Special').order_by('student_id')
    course = Course.objects.get(course_code= course_code)
    if course.course_type == 'Lab':
        return HttpResponseRedirect(f'/examcommitte/exam_committe_lab_course_details/{course.course_code}/')
    if course.course_type == 'Viva':
        return HttpResponseRedirect(f'/examcommitte/exam_committe_viva_course_details/{course.course_code}/')
    if course.course_type == 'Project':
        return HttpResponseRedirect(f'/examcommitte/exam_committe_project_course_details/{course.course_code}/')
    if course.course_type == 'Research_Project':
        return HttpResponseRedirect(f'/examcommitte/exam_committte_research_project/{course_code}/')

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
    return render(request, 'examcommite/course_details.html', context)  

def course_teacher_marks(request, course_code):
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
    return render(request, 'examcommite/course_teacher_marks.html', context)

def external_teacher_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    count = 0
    backLogStudents = {}
    regularStudents = {}
    specialStudents = {}
    for stu in regular_students:
        student_details = {}
        external_teacher_marks = External_teacher_marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        marks = 0
        for c in external_teacher_marks:
            marks = c.marks
        student_details['marks'] = marks
        regularStudents[stu] = student_details
        count += 1
    for stu in backLog_students:
        count += 1
        student_details = {}
        external_teacher_marks = External_teacher_marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        marks = 0
        for c in external_teacher_marks:
            marks = c.marks
        student_details['marks'] = marks
        student_details['count'] = count
        backLogStudents[stu] = student_details
    for stu in special_students:
        count += 1
        student_details = {}
        external_teacher_marks = External_teacher_marks.objects.filter(student_id= stu.student_id, course_code= course_code)
        marks = 0
        for c in external_teacher_marks:
            marks = c.marks
        student_details['marks'] = marks
        student_details['count'] = count
        specialStudents[stu] = student_details
    if request.method == 'POST':
        for r in regular_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        for r in backLog_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        for r in special_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        return HttpResponseRedirect(f"/examcommitte/details_external_teacher_marks/{course_code}")
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'regularStudents': regularStudents,
        'backLogStudents': backLogStudents,
        'specialStudents': specialStudents,
    }
    return render(request, 'examcommite/external_teacher_marks.html', context)

def details_external_teacher_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'regular_students': regular_students,
        'backLog_students': backLog_students,
        'special_students': special_students,
    }
    return render(request, 'examcommite/details_external_teacher_marks.html', context)

def edit_external_teacher_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = External_teacher_marks.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    if request.method == 'POST':
        for r in regular_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        for r in backLog_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        for r in special_students:
            data = request.POST.get(f'totalMark_{r.student_id}')
            if data:
                student_id = r.student_id
                course_code = course_code
                marks = float(data)
                rem = Teacher_Student_Info.objects.get(student_id= student_id, course_code= course_code)
                remarks = rem.remarks
                session = r.session
                check = External_teacher_marks.objects.filter(student_id=student_id, course_code=course_code)
                flag = False
                for c in check:
                    flag = True
                    id = c.id
                if flag == True:
                    data = External_teacher_marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
                else:
                    data = External_teacher_marks(
                        student_id = student_id,
                        course_code = course_code,
                        marks = marks,
                        remarks = remarks,
                        session = session
                    )
                    data.save()
        return HttpResponseRedirect(f'/examcommitte/details_external_teacher_marks/{course_code}/')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'regular_students': regular_students,
        'backLog_students': backLog_students,
        'special_students': special_students,
    }
    return render(request, 'examcommite/edit_external_teacher_marks.html', context)

def compare_internal_external_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    students = Teacher_Student_Info.objects.filter(course_code = course_code).order_by('student_id')
    third_examine_students = {}
    all_teacher_marks = {}
    save_button = False
    for s in students:
        course_teacher_mark = Theory_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_teacher_marks.objects.get(student_id= s.student_id, course_code= course_code)
        tem_checker = Third_Examinner_Marks.objects.filter(student_id= s.student_id, course_code= course_code)
        temark = 0
        for c in tem_checker:
            temark = c.marks
        dif = abs((course_teacher_mark.total_marks) - (external_teacher_mark.marks))
        average_marks = ((course_teacher_mark.total_marks) + (external_teacher_mark.marks))/2
        third_examiner_mark = False
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_marks, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.marks, 'third_examiner_mark': third_examiner_mark, 'temark': temark}
    
    if request.method == 'POST':
        for key, value in third_examine_students.items():
            data = request.POST.get(f'totalMark_{key.student_id}')
            if data:
                marks = float(data)
                student_id = key.student_id
                course_code = course_code
                session = key.session
                data = Third_Examinner_Marks(
                    student_id = student_id,
                    course_code = course_code,
                    session = session,
                    marks = marks
                )
                checker = Third_Examinner_Marks.objects.filter(student_id = student_id, course_code= course_code)
                flag = False
                for c in checker:
                    flag = True
                    id = c.id
                if flag == True:
                    data = Third_Examinner_Marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        session = session,
                        marks = marks
                    )
                    data.save()
                else:
                    data.save()
        return HttpResponseRedirect(f'/examcommitte/show_all_marks/{course_code}/')
    
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'all_teacher_marks': all_teacher_marks,
        'save_button': save_button,
    }
    return render(request, 'examcommite/compare_internal_external_marks.html', context)

def edit_third_examinner_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    third_examine_students = {}
    all_teacher_marks = {}
    save_button = False
    for s in regular_students:
        course_teacher_mark = Theory_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_teacher_marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_marks) - (external_teacher_mark.marks))
        average_marks = ((course_teacher_mark.total_marks) + (external_teacher_mark.marks))/2
        third_examiner_mark = False
        prev_value = 0
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
            value = Third_Examinner_Marks.objects.filter(student_id= s.student_id, course_code= course_code)
            for v in value:
                prev_value = v.marks
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_marks, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.marks, 'third_examiner_mark': third_examiner_mark, 'prev_value': prev_value}
    for s in backLog_students:
        course_teacher_mark = Theory_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_teacher_marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_marks) - (external_teacher_mark.marks))
        average_marks = ((course_teacher_mark.total_marks) + (external_teacher_mark.marks))/2
        third_examiner_mark = False
        prev_value = 0
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
            value = Third_Examinner_Marks.objects.filter(student_id= s.student_id, course_code= course_code)
            for v in value:
                prev_value = v.marks
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_marks, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.marks, 'third_examiner_mark': third_examiner_mark, 'prev_value': prev_value}
    for s in special_students:
        course_teacher_mark = Theory_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_teacher_marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_marks) - (external_teacher_mark.marks))
        average_marks = ((course_teacher_mark.total_marks) + (external_teacher_mark.marks))/2
        third_examiner_mark = False
        prev_value = 0
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
            value = Third_Examinner_Marks.objects.filter(student_id= s.student_id, course_code= course_code)
            for v in value:
                prev_value = v.marks
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_marks, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.marks, 'third_examiner_mark': third_examiner_mark, 'prev_value': prev_value}
    
    if request.method == 'POST':
        for key, value in third_examine_students.items():
            data = request.POST.get(f'totalMark_{key.student_id}')
            if data:
                marks = float(data)
                student_id = key.student_id
                course_code = course_code
                session = key.session
                data = Third_Examinner_Marks(
                    student_id = student_id,
                    course_code = course_code,
                    session = session,
                    marks = marks
                )
                checker = Third_Examinner_Marks.objects.filter(student_id = student_id, course_code= course_code)
                flag = False
                for c in checker:
                    flag = True
                    id = c.id
                if flag == True:
                    data = Third_Examinner_Marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        session = session,
                        marks = marks
                    )
                    data.save()
                else:
                    data.save()
        return HttpResponseRedirect(f'/examcommitte/show_all_marks/{course_code}/')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'all_teacher_marks': all_teacher_marks,
        'save_button':save_button,
    }
    return render(request, 'examcommite/edit_third_examinner_mark.html', context)

def show_all_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    student_marks = {}
    for student in regular_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2  
        
        student_marks[student] = {'course_teacher_mark': course_teacher_mark, 'external_teacher_mark': external_teacher_mark, 
        'third_examinner_mark': third_examinner_mark, 'average_mark': average_mark}
    for student in backLog_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2  
        
        student_marks[student] = {'course_teacher_mark': course_teacher_mark, 'external_teacher_mark': external_teacher_mark, 
        'third_examinner_mark': third_examinner_mark, 'average_mark': average_mark}
    for student in special_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2  
        
        student_marks[student] = {'course_teacher_mark': course_teacher_mark, 'external_teacher_mark': external_teacher_mark, 
        'third_examinner_mark': third_examinner_mark, 'average_mark': average_mark}
       
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'student_marks': student_marks,
    }
    return render(request, 'examcommite/show_all_marks.html', context)

def mark_sheet_details(request, course_code):
    course = Course.objects.get(course_code= course_code)
    credit = course.credit
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'Special').order_by('student_id')
    mark_sheets = {}
    for student in regular_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        s = Student.objects.get(student_id = student.student_id)
        full_name = s.first_name + " " + s.last_name
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2    
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        ct_marks = 0
        attendence_mark = 0
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        total_marks = ct_marks + attendence_mark + average_mark
        total_marks = math.ceil(total_marks)
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
        PS = credit * GP
        mark_sheets[student] = {'ct_marks': ct_marks, 'attendence_mark': attendence_mark, 'full_name': full_name,
        'average_mark': average_mark, 'total_marks': total_marks, 'LG': LG, 'GP': GP, 'PS': PS}
        data = Final_MarkSheet_Theory_Course(
            student_id = s.student_id,
            student_name = full_name,
            session = s.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = student.remarks,
            hall = s.hall,
            ct_marks = ct_marks,
            attendence_mark = attendence_mark,
            total_marks = total_marks,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Theory_Course.objects.filter(student_id = s.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Theory_Course(
                id = id,
                student_id = s.student_id,
                student_name = full_name,
                session = s.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                credits = course.credit,
                remarks = student.remarks,
                hall = s.hall,
                ct_marks = ct_marks,
                attendence_mark = attendence_mark,
                total_marks = total_marks,
                GP = GP,
                PS = PS,
                LG = LG,
            )
            data.save()
        else:
            data.save()
    for student in backLog_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        s = Student.objects.get(student_id = student.student_id)
        full_name = s.first_name + " " + s.last_name
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2    
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        ct_marks = 0
        attendence_mark = 0
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        total_marks = ct_marks + attendence_mark + average_mark
        total_marks = math.ceil(total_marks)
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
        PS = credit * GP
        mark_sheets[student] = {'ct_marks': ct_marks, 'attendence_mark': attendence_mark, 'full_name': full_name,
        'average_mark': average_mark, 'total_marks': total_marks, 'LG': LG, 'GP': GP, 'PS': PS}
        data = Final_MarkSheet_Theory_Course(
            student_id = s.student_id,
            student_name = full_name,
            session = s.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = student.remarks,
            hall = s.hall,
            ct_marks = ct_marks,
            attendence_mark = attendence_mark,
            total_marks = total_marks,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Theory_Course.objects.filter(student_id = s.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Theory_Course(
                id = id,
                student_id = s.student_id,
                student_name = full_name,
                session = s.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                credits = course.credit,
                remarks = student.remarks,
                hall = s.hall,
                ct_marks = ct_marks,
                attendence_mark = attendence_mark,
                total_marks = total_marks,
                GP = GP,
                PS = PS,
                LG = LG,
            )
            data.save()
        else:
            data.save()
    for student in special_students:
        course_teacher_marks = Theory_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_teacher_marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        s = Student.objects.get(student_id = student.student_id)
        full_name = s.first_name + " " + s.last_name
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_marks
        for mark in external_teacher_marks:
            external_teacher_mark = mark.marks
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2    
        ct_and_attendence_marks = Attendence_and_CT_Mark.objects.filter(student_id = student.student_id, course_code = course_code)
        ct_marks = 0
        attendence_mark = 0
        for mark in ct_and_attendence_marks:
            ct_marks = mark.ct_marks
            attendence_mark = mark.attendence_marks
        total_marks = ct_marks + attendence_mark + average_mark
        total_marks = math.ceil(total_marks)
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
        PS = credit * GP
        mark_sheets[student] = {'ct_marks': ct_marks, 'attendence_mark': attendence_mark, 'full_name': full_name,
        'average_mark': average_mark, 'total_marks': total_marks, 'LG': LG, 'GP': GP, 'PS': PS}
        data = Final_MarkSheet_Theory_Course(
            student_id = s.student_id,
            student_name = full_name,
            session = s.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = student.remarks,
            hall = s.hall,
            ct_marks = ct_marks,
            attendence_mark = attendence_mark,
            total_marks = total_marks,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_Theory_Course.objects.filter(student_id = s.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_Theory_Course(
                id = id,
                student_id = s.student_id,
                student_name = full_name,
                session = s.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                credits = course.credit,
                remarks = student.remarks,
                hall = s.hall,
                ct_marks = ct_marks,
                attendence_mark = attendence_mark,
                total_marks = total_marks,
                GP = GP,
                PS = PS,
                LG = LG,
            )
            data.save()
            messages.success(request, 'updated')
        else:
            data.save()
            messages.success(request, 'save')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'mark_sheets': mark_sheets,
    }
    return render(request, 'examcommite/mark_sheet_details.html', context)

def exam_committte_research_project(request, course_code):
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks='Special').order_by('student_id')
    course = Course.objects.get(course_code= course_code)
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
    return render(request, 'examcommite/research_project_details.html', context)

def external_teacher_research_project_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
    checker = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code)
    for c in checker:
        return HttpResponseRedirect(f'/examcommitte/edit_external_research_project_marks/{course_code}/')
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
            data = External_Teacher_Research_Project_Marks(
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
            checker = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = External_Teacher_Research_Project_Marks(
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
            data = External_Teacher_Research_Project_Marks(
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
            checker = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = External_Teacher_Research_Project_Marks(
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
            data = External_Teacher_Research_Project_Marks(
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
            checker = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = External_Teacher_Research_Project_Marks(
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
        return HttpResponseRedirect(f'/examcommitte/show_external_research_project_marks/{course_code}')
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
    return render(request, 'examcommite/external_teacher_research_project_marks.html', context)

def show_external_research_project_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, remarks="Regular").order_by('student_id')
    backLog_students = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, remarks="BackLog").order_by('student_id')
    special_students = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, remarks="Special").order_by('student_id')
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
    return render(request, 'examcommite/show_external_research_project_marks.html', context)

def edit_external_research_project_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, remarks='Regular').order_by('student_id')
    backLog_students = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, remarks='BackLog').order_by('student_id')
    special_students = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, remarks='Special').order_by('student_id')
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
            data = External_Teacher_Research_Project_Marks(
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
            checker = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = External_Teacher_Research_Project_Marks(
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
            data = External_Teacher_Research_Project_Marks(
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
            checker = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = External_Teacher_Research_Project_Marks(
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
            data = External_Teacher_Research_Project_Marks(
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
            checker = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id = student.student_id)
            flag = False
            for c in checker:
                flag = True
                id = c.id
            if flag == True:
                data = External_Teacher_Research_Project_Marks(
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
        return HttpResponseRedirect(f'/examcommitte/show_external_research_project_marks/{course_code}')
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
    return render(request, 'examcommite/edit_external_research_project_marks.html', context)

def course_teacher_research_project_marks(request, course_code):
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
    return render(request, 'examcommite/course_teacher_research_project_marks.html', context)

def check_third_examinner_research_project_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    checker = Third_Examinner_ResearchProject_Marks.objects.filter(course_code= course_code)
    for check in checker:
        return HttpResponseRedirect(f'/examcommitte/edit_third_examinner_research_project_mark/{course_code}/')
    students = Teacher_Student_Info.objects.filter(course_code = course_code).order_by('student_id')
    third_examine_students = {}
    all_teacher_marks = {}
    save_button = False
    for s in students:
        course_teacher_mark = Research_Project_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_Teacher_Research_Project_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_mark) - (external_teacher_mark.total_mark))
        average_marks = ((course_teacher_mark.total_mark) + (external_teacher_mark.total_mark))/2
        third_examiner_mark = False
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_mark, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.total_mark, 'third_examiner_mark': third_examiner_mark}
    
    if request.method == 'POST':
        for key, value in third_examine_students.items():
            data = request.POST.get(f'totalMark_{key.student_id}')
            if data:
                marks = float(data)
                student_id = key.student_id
                course_code = course_code
                session = key.session
                data = Third_Examinner_ResearchProject_Marks(
                    student_id = student_id,
                    course_code = course_code,
                    session = session,
                    marks = marks
                )
                checker = Third_Examinner_ResearchProject_Marks.objects.filter(student_id = student_id, course_code= course_code)
                flag = False
                for c in checker:
                    flag = True
                    id = c.id
                if flag == True:
                    data = Third_Examinner_ResearchProject_Marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        session = session,
                        marks = marks
                    )
                    data.save()
                else:
                    data.save()
        return HttpResponseRedirect(f'/examcommitte/show_research_projects_all_marks/{course_code}/')
    
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'all_teacher_marks': all_teacher_marks,
        'save_button': save_button,
    }
    return render(request, 'examcommite/check_third_examinner_research_project_marks.html', context)

def show_research_projects_all_marks(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    student_marks = {}
    for student in regular_students:
        course_teacher_marks = Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_ResearchProject_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_mark
        for mark in external_teacher_marks:
            external_teacher_mark = mark.total_mark
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 100
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2  
        
        student_marks[student] = {'course_teacher_mark': course_teacher_mark, 'external_teacher_mark': external_teacher_mark, 
        'third_examinner_mark': third_examinner_mark, 'average_mark': average_mark}
    for student in backLog_students:
        course_teacher_marks = Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_ResearchProject_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_mark
        for mark in external_teacher_marks:
            external_teacher_mark = mark.total_mark
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2  
        
        student_marks[student] = {'course_teacher_mark': course_teacher_mark, 'external_teacher_mark': external_teacher_mark, 
        'third_examinner_mark': third_examinner_mark, 'average_mark': average_mark}
    for student in special_students:
        course_teacher_marks = Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_ResearchProject_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_mark
        for mark in external_teacher_marks:
            external_teacher_mark = mark.total_mark
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2  
        
        student_marks[student] = {'course_teacher_mark': course_teacher_mark, 'external_teacher_mark': external_teacher_mark, 
        'third_examinner_mark': third_examinner_mark, 'average_mark': average_mark}
       
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'student_marks': student_marks,
    }
    return render(request, 'examcommite/show_research_projects_all_marks.html', context)

def edit_third_examinner_research_project_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    regular_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code = course_code, remarks= 'Special').order_by('student_id')
    third_examine_students = {}
    all_teacher_marks = {}
    save_button = False
    for s in regular_students:
        course_teacher_mark = Research_Project_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_Teacher_Research_Project_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_mark) - (external_teacher_mark.total_mark))
        average_marks = ((course_teacher_mark.total_mark) + (external_teacher_mark.total_mark))/2
        third_examiner_mark = False
        prev_value = 0
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
            value = Third_Examinner_ResearchProject_Marks.objects.filter(student_id= s.student_id, course_code= course_code)
            for v in value:
                prev_value = v.marks
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_mark, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.total_mark, 'third_examiner_mark': third_examiner_mark, 'prev_value': prev_value}
    for s in backLog_students:
        course_teacher_mark = Research_Project_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_Teacher_Research_Project_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_mark) - (external_teacher_mark.total_mark))
        average_marks = ((course_teacher_mark.total_mark) + (external_teacher_mark.total_mark))/2
        third_examiner_mark = False
        prev_value = 0
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
            value = Third_Examinner_ResearchProject_Marks.objects.filter(student_id= s.student_id, course_code= course_code)
            for v in value:
                prev_value = v.marks
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_mark, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.total_mark, 'third_examiner_mark': third_examiner_mark, 'prev_value': prev_value}
    for s in special_students:
        course_teacher_mark = Research_Project_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        external_teacher_mark = External_Teacher_Research_Project_Marks.objects.get(student_id= s.student_id, course_code= course_code)
        dif = abs((course_teacher_mark.total_mark) - (external_teacher_mark.total_mark))
        average_marks = ((course_teacher_mark.total_mark) + (external_teacher_mark.total_mark))/2
        third_examiner_mark = False
        prev_value = 0
        if dif >= 14:
            third_examiner_mark = True
            save_button = True
            third_examine_students[s] = dif
            value = Third_Examinner_ResearchProject_Marks.objects.filter(student_id= s.student_id, course_code= course_code)
            for v in value:
                prev_value = v.marks
        
        all_teacher_marks[s] = {'course_teacher_mark':course_teacher_mark.total_mark, 'average_marks': average_marks,
        'external_teacher_mark': external_teacher_mark.total_mark, 'third_examiner_mark': third_examiner_mark, 'prev_value': prev_value}
    
    if request.method == 'POST':
        for key, value in third_examine_students.items():
            data = request.POST.get(f'totalMark_{key.student_id}')
            if data:
                marks = float(data)
                student_id = key.student_id
                course_code = course_code
                session = key.session
                data = Third_Examinner_ResearchProject_Marks(
                    student_id = student_id,
                    course_code = course_code,
                    session = session,
                    marks = marks
                )
                checker = Third_Examinner_ResearchProject_Marks.objects.filter(student_id = student_id, course_code= course_code)
                flag = False
                for c in checker:
                    flag = True
                    id = c.id
                if flag == True:
                    data = Third_Examinner_ResearchProject_Marks(
                        id = id,
                        student_id = student_id,
                        course_code = course_code,
                        session = session,
                        marks = marks
                    )
                    data.save()
                else:
                    data.save()
        return HttpResponseRedirect(f'/examcommitte/show_research_projects_all_marks/{course_code}/')
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_name': course.course_name,
        'credit': course.credit,
        'all_teacher_marks': all_teacher_marks,
        'save_button':save_button,
    }
    return render(request, 'examcommite/edit_third_examinner_research_project_mark.html', context)

def final_consoilated_research_project_marksheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    credit = course.credit
    regular_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'Regular').order_by('student_id')
    backLog_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'BackLog').order_by('student_id')
    special_students = Teacher_Student_Info.objects.filter(course_code= course_code, remarks= 'Special').order_by('student_id')
    mark_sheets = {}
    for student in regular_students:
        course_teacher_marks = Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_ResearchProject_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        s = Student.objects.get(student_id = student.student_id)
        full_name = s.first_name + " " + s.last_name
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_mark
        for mark in external_teacher_marks:
            external_teacher_mark = mark.total_mark
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2    
        
        total_marks = average_mark
        total_marks = math.ceil(total_marks)
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
        PS = credit * GP
        mark_sheets[student] = {'full_name': full_name,'total_marks': total_marks, 'LG': LG, 'GP': GP, 'PS': PS}
        data = Final_MarkSheet_ResearchProject_Course(
            student_id = s.student_id,
            student_name = full_name,
            session = s.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = student.remarks,
            hall = s.hall,
            total_marks = total_marks,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_ResearchProject_Course.objects.filter(student_id = s.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_ResearchProject_Course(
                id = id,
                student_id = s.student_id,
                student_name = full_name,
                session = s.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                credits = course.credit,
                remarks = student.remarks,
                hall = s.hall,
                total_marks = total_marks,
                GP = GP,
                PS = PS,
                LG = LG,
            )
            data.save()
        else:
            data.save()
    for student in backLog_students:
        course_teacher_marks = Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_ResearchProject_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        s = Student.objects.get(student_id = student.student_id)
        full_name = s.first_name + " " + s.last_name
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_mark
        for mark in external_teacher_marks:
            external_teacher_mark = mark.total_mark
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2    
        
        total_marks = average_mark
        total_marks = math.ceil(total_marks)
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
        PS = credit * GP
        mark_sheets[student] = {'full_name': full_name, 'total_marks': total_marks, 'LG': LG, 'GP': GP, 'PS': PS}
        data = Final_MarkSheet_ResearchProject_Course(
            student_id = s.student_id,
            student_name = full_name,
            session = s.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = student.remarks,
            hall = s.hall,
            total_marks = total_marks,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_ResearchProject_Course.objects.filter(student_id = s.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_ResearchProject_Course(
                id = id,
                student_id = s.student_id,
                student_name = full_name,
                session = s.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                credits = course.credit,
                remarks = student.remarks,
                hall = s.hall,
                total_marks = total_marks,
                GP = GP,
                PS = PS,
                LG = LG,
            )
            data.save()
        else:
            data.save()
    for student in special_students:
        course_teacher_marks = Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        external_teacher_marks = External_Teacher_Research_Project_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        third_examinner_marks = Third_Examinner_ResearchProject_Marks.objects.filter(course_code= course_code, student_id= student.student_id)
        s = Student.objects.get(student_id = student.student_id)
        full_name = s.first_name + " " + s.last_name
        course_teacher_mark = 0 
        external_teacher_mark=0
        third_examinner_mark = 0
        average_mark = 0
        for mark in course_teacher_marks:
            course_teacher_mark = mark.total_mark
        for mark in external_teacher_marks:
            external_teacher_mark = mark.total_mark
        for mark in third_examinner_marks:
            third_examinner_mark = mark.marks
        if third_examinner_mark == 0:
            average_mark = (course_teacher_mark + external_teacher_mark)/2
        else:
            min = 70
            list=[]
            list.append(course_teacher_mark)
            list.append(external_teacher_mark)
            list.append(third_examinner_mark)
            list.sort()
            x1 = abs(list[0] - list[1])
            x2 = abs(list[1] - list[2])
            if x1 < x2:
                average_mark = (list[0] + list[1])/2
            elif x2 < x1:
                average_mark = (list[1] + list[2])/2
            else:
                total1 = list[0] + list[2]
                total2 = list[1] + list[2]
                if total1 >= total2:
                    average_mark = total1/2
                else:
                    average_mark = total2/2    
        
        total_marks = average_mark
        total_marks = math.ceil(total_marks)
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
        PS = credit * GP
        mark_sheets[student] = {'full_name': full_name, 'total_marks': total_marks, 'LG': LG, 'GP': GP, 'PS': PS}
        data = Final_MarkSheet_ResearchProject_Course(
            student_id = s.student_id,
            student_name = full_name,
            session = s.session,
            semester_no = course.semister_no,
            course_code = course.course_code,
            credits = course.credit,
            remarks = student.remarks,
            hall = s.hall,
            total_marks = total_marks,
            GP = GP,
            PS = PS,
            LG = LG,
        )
        checker = Final_MarkSheet_ResearchProject_Course.objects.filter(student_id = s.student_id, course_code= course_code)
        flag = False
        for c in checker:
            id = c.id
            flag = True
        if flag == True:
            data = Final_MarkSheet_ResearchProject_Course(
                id = id,
                student_id = s.student_id,
                student_name = full_name,
                session = s.session,
                semester_no = course.semister_no,
                course_code = course.course_code,
                credits = course.credit,
                remarks = student.remarks,
                hall = s.hall,
                total_marks = total_marks,
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
        'c_name': course.course_name,
        'credit': course.credit,
        'mark_sheets': mark_sheets,
    }
    return render(request, 'examcommite/final_consoilated_research_project_marksheet.html', context)

def exam_committe_lab_course_details(request, course_code):
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
    return render(request, 'examcommite/exam_committe_lab_course_details.html', context)

def exam_committe_project_course_details(request, course_code):
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
    return render(request, 'examcommite/exam_committe_project_course_details.html', context)

def exam_committe_viva_course_details(request, course_code):
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
    return render(request, 'examcommite/exam_committe_viva_course_details.html',context)

def semester_final_result(request, semester_no):
    courses = Course.objects.filter(semister_no = semester_no)
    students = Registration_By_Semester.objects.filter(semester_name = semester_no)
    student_info ={}
    for student in students:
        course_details = {}
        credit_earn = 0
        total_credit = 0
        tps = 0
        stu = Student.objects.get(student_id= student.student_id)
        stu_courses = Teacher_Student_Info.objects.filter(student_id= student.student_id, semester= semester_no)
        for c in courses:
            course = Course.objects.get(course_code= c.course_code)
            
            ps = 0
            total_marks = 0
            if course.course_type == 'Theory':
                point_secures = Final_MarkSheet_Theory_Course.objects.filter(student_id= student.student_id, course_code = course.course_code)
                for c in point_secures:
                    ps = c.PS
                    total_marks = c.total_marks
            if course.course_type == 'Lab':
                point_secures = Final_MarkSheet_Lab_Course.objects.filter(student_id= student.student_id, course_code = course.course_code)
                for c in point_secures:
                    ps = c.PS
                    total_marks = c.total_marks

            if course.course_type == 'Viva':
                point_secures = Final_MarkSheet_Viva_Course.objects.filter(student_id= student.student_id, course_code = course.course_code)
                for c in point_secures:
                    ps = c.PS
                    total_marks = c.total_marks

            if course.course_type == 'Project':
                point_secures = Final_MarkSheet_Project_Course.objects.filter(student_id= student.student_id, course_code = course.course_code)
                for c in point_secures:
                    ps = c.PS
                    total_marks = c.total_marks

            if course.course_type == 'Research_Project':
                point_secures = Final_MarkSheet_Project_Course.objects.filter(student_id= student.student_id, course_code = course.course_code)
                for c in point_secures:
                    ps = c.PS
                    total_marks = c.total_marks

            flag = False
            credit = 0
            
            for main_course in stu_courses:
                if main_course.course_code == c.course_code:
                    flag = True
                    credit = main_course.credit
                    total_credit += credit
                    break
                
            if flag == True:
                tps += ps
                if ps == 0:
                    credit_earn += 0
                else:
                    credit_earn += main_course.credit
                total_marks = math.ceil(total_marks)
                if total_marks >= 80:
                    c_lg = 'A+'
                    c_gp = 4.00
                    c_ps = credit * c_gp
                    c_ps = "{:.2f}".format(c_ps)

                elif total_marks >= 75:
                    c_lg = 'A'
                    c_gp = 3.75
                    c_ps = credit * c_gp
                    c_ps = "{:.2f}".format(c_ps)

                elif total_marks >= 70:
                    c_lg = 'A-'
                    c_gp = 3.50
                    c_ps = credit * c_gp
                    c_ps = "{:.2f}".format(c_ps)

                elif total_marks >= 65:
                    c_lg = 'B+'
                    c_gp = 3.25
                    c_ps = credit * c_gp
                    c_ps = "{:.2f}".format(c_ps)

                elif total_marks >= 60:
                    c_lg = 'B'
                    c_gp = 3.00
                    c_ps = credit * c_gp
                    c_ps = "{:.2f}".format(c_ps)

                elif total_marks >= 55:
                    c_lg = 'B-'
                    c_gp = 2.75
                    c_ps = credit * c_gp
                    c_ps = "{:.2f}".format(c_ps)

                elif total_marks >= 50:
                    c_lg = 'C+'
                    c_gp = 2.50
                    c_ps = credit * c_gp
                    c_ps = "{:.2f}".format(c_ps)

                elif total_marks >= 45:
                    c_lg = 'C'
                    c_gp = 2.25
                    c_ps = credit * c_gp
                    c_ps = "{:.2f}".format(c_ps)

                elif total_marks >= 40:
                    c_lg = 'D'
                    c_gp = 2.00
                    c_ps = credit * c_gp
                    c_ps = "{:.2f}".format(c_ps)

                else:
                    c_lg = 'F'
                    c_gp = 0.00
                    c_ps = credit * c_gp
                    c_ps = "{:.2f}".format(c_ps)
                course_details[f'{c.course_code}'] = {'total_mark': total_marks, 'c_lg': c_lg, 'c_gp': c_gp, 'c_ps': c_ps}
            else:
                course_details[f'{c.course_code}'] = {'total_mark': '', 'c_lg': '', 'c_gp': '', 'c_ps': ''}

        if credit_earn == 0:
            gpa = 0
        else:
            gpa = tps/credit_earn
        if gpa >= 4.00:
            result = 'A+'
        elif gpa >= 3.75:
            result = 'A'
        elif gpa >= 3.5:
            result = 'A-'
        elif gpa >= 3.25:
            result = 'B+'
        elif gpa >= 3.00:
            result = 'B'
        elif gpa >= 2.75:
            result = 'B-'
        elif gpa >= 2.5:
            result = 'C+'
        elif gpa >= 2.25:
            result = 'C'
        elif gpa >= 2.00:
            result = 'D'
        else:
            result = 'F'
        gpa = "{:.2f}".format(gpa)
        # final_result = {'total_credit': total_credit, 'credit_earn': credit_earn, 'tps': tps, 'gpa': gpa, 'result': result}
        course_details['total_credit'] = total_credit
        course_details['credit_earn'] = credit_earn
        course_details['tps'] = tps
        course_details['gpa'] = gpa
        course_details['result'] = result
        student_info[stu] =  course_details
       
    context = {
        'semester_no': semester_no,
        'courses': courses,
        'total_credit': total_credit,
        'students': students,
        'student_info': student_info,
    }
    return render(request, 'examcommite/semester_final_result.html', context)