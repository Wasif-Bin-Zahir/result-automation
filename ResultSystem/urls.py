from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('student/', include('student.urls')),
    path('faculty/', include('faculty.urls')),
    path('stuff/', include('stuff.urls')),
    path('chairman/', include('chairman.urls')),
    path('exam_controller/', include('examcontroller.urls')),
    path('examcommitte/', include('examcommite.urls')),
   
    path('', views.home_page, name="home"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

