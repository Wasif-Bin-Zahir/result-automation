from django.shortcuts import render, HttpResponseRedirect
from .models import ExamController, Student, Teacher, Teacher_email, UserManager, OfficeStuff, ExamCommitte
from .forms import StudentRegForm, LoginForm, TeacherRegForm, OfficeStuffRegForm, ExamControllerRegForm, \
    ExamCommitteRegForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import Group
from .models import User
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserChangeForm

user_model = get_user_model()


# # signup


def student_signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = StudentRegForm(request.POST, request.FILES)
            if fm.is_valid():
                email = fm.cleaned_data['email']
                student_id = fm.cleaned_data['student_id']
                if (email[0] != 'c' and email[1] != 'e' and email[7] != '@' and email[8] != 'm' and email[9] != 'b' and
                        email[10] != 's' and email[11] != 't' and email[12] != 'u'):
                    messages.warning(
                        request, 'Please enter the valid email addres return')
                    return HttpResponseRedirect('/auth/student_signup/')

                if (student_id[0] != 'C' and student_id[1] != 'E'):
                    messages.info(request, 'Please enter the valid student id')
                    return HttpResponseRedirect('/auth/student_signup/')
                # user = fm.save(commit=False)
                # user.is_active = False
                # user.save()
                # current_site = get_current_site(request)
                # mail_subject = 'Activate your account'
                # message = render_to_string('authentication/account.html', {
                #     'user': user,
                #     'domain': current_site.domain,
                #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #     'token': default_token_generator.make_token(user),
                # })
                # send_mail = fm.cleaned_data.get('email')
                # email = EmailMessage(mail_subject, message, to=[send_mail])
                # email.send()
                # fm.save()
                # messages.success(request, 'Successfully created account')
                # messages.success(request, 'Activate your account from email')
                return HttpResponseRedirect('/auth/login/')
        else:
            fm = StudentRegForm()
        return render(request, 'authentication/student_signup.html', {'form': fm})
    else:
        return HttpResponseRedirect('/')


# # activate your account

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user_model._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account activated now you can login')
        return HttpResponseRedirect('/auth/login/')
    else:
        messages.warning(request, 'activation link is invalid')
        return HttpResponseRedirect('/')


# login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = LoginForm(data=request.POST)
            if fm.is_valid():
                mail = fm.cleaned_data['email']
                psw = fm.cleaned_data['password']
                user = authenticate(email=mail, password=psw)
                if user is not None:
                    login(request, user)
                    print(mail, psw)
                    messages.success(request, 'Login Successfull!!')
                    if user.is_admin:
                        return HttpResponseRedirect('/chairman/profile/')
                    teacher = Teacher.objects.filter(email=mail)
                    for t in teacher:
                        return HttpResponseRedirect('/faculty/profile/')

                    student = Student.objects.filter(email=mail)
                    for s in student:
                        return HttpResponseRedirect('/student/profile/')

                    office = OfficeStuff.objects.filter(email=mail)
                    for s in office:
                        return HttpResponseRedirect('/stuff/profile/')
                    exam_controller = ExamController.objects.filter(email=mail)
                    for s in exam_controller:
                        return HttpResponseRedirect('/exam_controller/profile/')

                    exam_committe = ExamCommitte.objects.filter(email=mail)
                    for s in exam_committe:
                        return HttpResponseRedirect('/examcommitte/profile/')
                else:
                    messages.error(request, 'wrong user enter correct one')
                    fm = LoginForm()
                    return render(request, 'authentication/login.html', {'form': fm})
            else:
                messages.warning(request, 'wrong user!!!!!!!!!!!!')
                return HttpResponseRedirect('/auth/login/')
        else:
            fm = LoginForm()
        return render(request, 'authentication/login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/')


# logout

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')


def check_mail(request):
    return render(request, 'authentication/gmailMessage.html')


def teacher_signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = TeacherRegForm(request.POST, request.FILES)
            if form.is_valid():
                mail = form.cleaned_data['email']
                flag = False
                for m in Teacher_email.objects.all():
                    if m.email == mail:
                        flag = True
                        break
                if flag:
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account'
                    message = render_to_string('authentication/account.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    send_mail = form.cleaned_data.get('email')
                    email = EmailMessage(mail_subject, message, to=[send_mail])
                    email.send()
                    messages.success(request, 'Successfully created account')
                    messages.success(request, 'Activate your account from email')
                    return HttpResponseRedirect('/auth/login/')

            else:
                messages.info(request, 'Enter the correct value!!!')
        form = TeacherRegForm()
        return render(request, 'authentication/teacher_signup.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def office_stuff_signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = OfficeStuffRegForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('authentication/account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[send_mail])
                email.send()
                messages.success(request, 'Successfully created account')
                messages.success(request, 'Activate your account from email')
                return HttpResponseRedirect('/auth/gmail/')

            else:
                messages.info(request, 'Enter the correct value!!!')
        form = OfficeStuffRegForm()
        return render(request, 'authentication/officestuff_signup.html', {'form': form})
    return HttpResponseRedirect('/')


def exam_controller(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = ExamControllerRegForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                messages.info(request, 'Enter the correct value!!!')
        form = ExamControllerRegForm()
        return render(request, 'authentication/external_teacher.html', {'form': form})
    return HttpResponseRedirect('/')


def exam_committe(request):
    if request.method == 'POST':
        form = ExamCommitteRegForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Complete')
            return HttpResponseRedirect('/auth/exam_committe/')
    form = ExamCommitteRegForm()
    return render(request, 'authentication/examcommitte.html', {'form': form})
