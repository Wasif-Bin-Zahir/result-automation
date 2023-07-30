from django.urls import path
from . import views
 
urlpatterns = [
    path('exam_controller_pswreset/', views.exam_controller_pswreset, name="exam_controller_pswreset"),
    path('exam_controller_pswreset2/', views.exam_controller_pswreset2, name="exam_controller_pswreset2"),
    path('profile/', views.exam_controller_profile, name= "exam_controller_profile"),
    path('exam_controller_logout/', views.exam_controller_logout, name= "exam_controller_logout"),

]
