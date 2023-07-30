from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

urlpatterns = [
    path('student_signup/', views.student_signup, name="student_signup"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('gmail/', views.check_mail, name='mail'),
    path('teacher_signup/', views.teacher_signup, name="teacher_signup"),
    path('office_stuff_signup/', views.office_stuff_signup, name="office_stuff_signup"),
    path('exam_controller/', views.exam_controller, name="exam_controller"),
    path('exam_committe/', views.exam_committe, name="exam_committe"),

    #     # email verification
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('reset/password/', PasswordResetView.as_view(template_name='authentication/resetpassword.html'),
         name='password_reset'),
    path('reset/password/done/', PasswordResetDoneView.as_view(template_name='authentication/reset_password_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
         name='password_reset_complete'),

]
