from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _ 
from django import forms
from . models import Student, Teacher, OfficeStuff, ExamController, ExamCommitte

class StudentRegForm(UserCreationForm):
    password1 = forms.CharField(label="Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email',  'session',
        'student_id', 'profile_image', 'hall']

        labels = {'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'email': 'Institute Email',
                  'session': 'Session',
                  'student_id': 'Student ID',
                  'profile_image': 'Profile Image',
                  'hall': 'Attached Hall',
                  'password1': 'Password',
                  'password2': 'Confirm Password',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dept': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'hall': forms.Select(attrs={'class': 'form-control'}),
            'profile_image': forms.URLInput(attrs={'class': 'form-control'}),
        }
    
class LoginForm(forms.Form):
    email = forms.EmailField(widget= forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip= False, widget= forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

Interested_Field_CHOICES = (
    ('Machine Learning', 'Machine Learning'),
    ('Bioinformatics', 'Bioinformatics'),
    ('Image security', 'Image security'),
    ('Network Security', 'Machine Learning'),
    ('Data Structure and Analysis of Algorithms', 'Data Structure and Analysis of Algorithms'),
    ('Logic Optimization Algorithms', 'Logic Optimization Algorithms'),
    ('Natural Language Processing', 'Natural Language Processing'),
    ('Data Mining', 'Data Mining'),
    ('Neural Network', 'Neural Network'),
    ('VLSI design', 'VLSI design'),
    ('Wavelet and PDE based image processing', 'Wavelet and PDE based image processing'),
    ('Medical Image Processing', 'Medical Image Processing'),
    ('Vehicular Ad Hoc Network', 'Vehicular Ad Hoc Network'),
    ('IoT', 'IoT'),
    ('Wireless Sensor Network', 'Wireless Sensor Network'),
    ('System Optimization', 'System Optimization'),
    ('Soft Computing Methods', 'Soft Computing Methods'),
    ('Human Computer Interaction', 'Human Computer Interaction'),
    ('Human Factors', 'Human Factors'),
    ('Network Security', 'Network Security'),
)

class TeacherRegForm(UserCreationForm):
    password1 = forms.CharField(label="Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    interested_field = forms.MultipleChoiceField(label= 'Interested Field', choices=Interested_Field_CHOICES, widget= forms.CheckboxSelectMultiple(attrs={'class': 'multiple'}))
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email',  'position',
        'profile_img','mobile_number','password1', 'password2', 'interested_field']

        labels = {'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'email': 'Email',
                  'profile_img': 'Profile Image',
                  'password1': 'Password',
                  'password2': 'Confirm Password',
                  'mobile_number': 'Mobile Number',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'interested_field': forms.TextInput(attrs={'class': 'form-control', 'id':'interst_field'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_img': forms.URLInput(attrs={'class': 'form-control'}),
        }

class OfficeStuffRegForm(UserCreationForm):
    password1 = forms.CharField(label="Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = OfficeStuff
        fields = ['first_name', 'last_name', 'email',  'position',
        'profile_img','mobile_number','password1', 'password2']

        labels = {'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'email': 'Email',
                  'profile_img': 'Profile Image',
                  'password1': 'Password',
                  'password2': 'Confirm Password',
                  'mobile_number': 'Mobile Number',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_img': forms.URLInput(attrs={'class': 'form-control'}),
        }

class ExamControllerRegForm(UserCreationForm):
    password1 = forms.CharField(label="Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = ExamController
        fields = ['first_name', 'last_name', 'email',
        'profile_img','mobile_number','password1', 'password2']

        labels = {'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'email': 'Email',
                  'profile_img': 'Profile Image',
                  'password1': 'Password',
                  'password2': 'Confirm Password',
                  'mobile_number': 'Mobile Number',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_img': forms.URLInput(attrs={'class': 'form-control'}),
        }

class ExamCommitteRegForm(UserCreationForm):
    password1 = forms.CharField(label="Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = ExamCommitte
        fields = ['first_name', 'last_name', 'email',
        'profile_img','mobile_number', 'password1', 'password2']

        labels = {'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'email': 'Email',
                  'profile_img': 'Profile Image',
                  'password1': 'Password',
                  'password2': 'Confirm Password',
                  'mobile_number': 'Mobile Number',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_img': forms.URLInput(attrs={'class': 'form-control'}),
        }
