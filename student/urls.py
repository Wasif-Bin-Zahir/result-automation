from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('profile/', views.student_profile, name= "student_profile"),
    path('logout/', views.student_logout, name= "student_logout"),
    path('student_pswreset/', views.student_password_reset, name= 'student_pswreset'),
   	path('student_pswreset2/', views.student_password_reset2, name= 'student_pswreset2'),
   	path('current_courses/', views.current_courses, name= 'current_courses'),
   	path('complete_courses/', views.complete_courses, name= 'complete_courses'),
   	path('course_registration/', views.course_registration, name= 'course_registration'),
   	path('student_special_course_registration/', views.student_special_course_registration, name= 'student_special_course_registration'),
   	path('application_form/', views.application_form, name= 'application_form'),
   	
]
