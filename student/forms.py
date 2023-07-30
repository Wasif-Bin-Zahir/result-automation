# from django.contrib.auth import views as auth_views
# from django import forms
# from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm
# from django.contrib.auth.models import User
# from django.utils.translation import gettext, gettext_lazy as _ 
# from django import forms
# from . models import Student

# class StudentRegForm(UserCreationForm):
#     password1 = forms.CharField(label="Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     class Meta:
#         model = Student
#         fields = ['username', 'email',  'session',
#         'student_id', 'profile_image', 'hall']

#         labels = {'username': 'User Name',
#                   'email': 'Institute Email',
#                   'session': 'Session',
#                   'student_id': 'Student ID',
#                   'profile_image': 'Profile Image',
#                   'hall': 'Attached Hall',
#                   'password1': 'Password',
#                   'password2': 'Confirm Password',
#         }
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'dept': forms.Select(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'session': forms.Select(attrs={'class': 'form-control'}),
#             'student_id': forms.TextInput(attrs={'class': 'form-control'}),
#             'hall': forms.Select(attrs={'class': 'form-control'}),
#             'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
#         }
    
# class LoginForm(AuthenticationForm):
#     username = UsernameField(widget= forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
#     password = forms.CharField(label=_("Password"), strip= False, widget= forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

