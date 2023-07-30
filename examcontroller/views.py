from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from authentication.models import *
from chairman.models import Course


# Create your views here.
def exam_controller_profile(request):
    email = request.user
    controller = ExamController.objects.filter(email = email)
    return render(request, 'examcontroller/profile.html', {'controller': controller})

def exam_controller_pswreset(request):
    if request.user.is_authenticated:
        res = ExamController.objects.filter(email= request.user)
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
                    return HttpResponseRedirect('/exam_controller/profile/')
            else:
                fm = PasswordChangeForm(request.user)
            return render(request, 'examcontroller/pswreset1.html', {'form': fm, 'faculty': res})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/') 

def exam_controller_pswreset2(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            res = ExamController.objects.filter(email= request.user)
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
                        return HttpResponseRedirect('/exam_controller/profile/')
                else:
                    fm = SetPasswordForm(request.user)
                return render(request, 'examcontroller/pswreset2.html', {'form': fm, 'faculty': res})
            else:
                return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

def current_courses(request):
    return HttpResponseRedirect(request, 'examcontroller/current_courses.html')

def exam_controller_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')

