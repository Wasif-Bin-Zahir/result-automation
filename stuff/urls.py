from django.urls import path
from . import views
 
urlpatterns = [
    path('profile/', views.stuff_profile, name= "stuff_profile"),
    path('logout/', views.stuff_logout, name= "stuff_logout"),
    path('stuff_pswreset/', views.stuff_password_reset, name= 'stuff_pswreset'),
   	path('stuff_pswreset2/', views.stuff_password_reset2, name= 'stuff_pswreset2'),
]
