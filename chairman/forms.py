from django import forms
from . models import Course, Running_Semester

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        labels = {
            'course_name': 'Course Name',
            'course_code': 'Course Code',
            'course_type': 'Course Type',
            'credit': 'Course Credit',
            'semister_no': 'Semester No',
            'course_teacher': 'Course Teacher'
        }
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'credit': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester_no': forms.Select(attrs={'class': 'form-control'}),
            'course_type': forms.Select(attrs={'class': 'form-control'}),
            'course_teacher': forms.Select(attrs={'class': 'form-control'}),
        }

class Running_Semester_Form(forms.ModelForm):
    class Meta:
        model = Running_Semester
        fields = '__all__'
        widgets = {
            'semester_no': forms.Select(attrs={'class': 'form-control'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
        }