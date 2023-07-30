from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from authentication.models import *

# Create your views here.
def stuff_profile(request):
    if request.user.is_authenticated:
        res = OfficeStuff.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            return render(request, 'stuff/profile.html')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

#logout
def stuff_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')


def stuff_password_reset(request):
    if request.user.is_authenticated:
        res = OfficeStuff.objects.filter(email= request.user)
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
                    return HttpResponseRedirect('/stuff/profile/')
            else:
                fm = PasswordChangeForm(request.user)
            return render(request, 'stuff/pswreset1.html', {'form': fm})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/') 

def stuff_password_reset2(request):
    if request.user.is_authenticated:
        res = OfficeStuff.objects.filter(email= request.user)
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
                    return HttpResponseRedirect('/stuff/profile/')
            else:
                fm = SetPasswordForm(request.user)
            return render(request, 'stuff/pswreset2.html', {'form': fm})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')