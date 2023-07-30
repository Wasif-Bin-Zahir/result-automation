from django.shortcuts import render, HttpResponseRedirect
from authentication.models import Student, Teacher, OfficeStuff, ExamController, ExamCommitte

def home_page(request):
	if not request.user.is_authenticated:
		return render(request, 'base.html')
	else:
		if request.user.is_admin:
			return HttpResponseRedirect('/chairman/profile/')
		if (Student.objects.filter(email= request.user)):
			return HttpResponseRedirect('/student/profile/')
		if (Teacher.objects.filter(email= request.user)):
			return HttpResponseRedirect('/faculty/profile/')
		if (OfficeStuff.objects.filter(email= request.user)):
			return HttpResponseRedirect('/stuff/profile/')
		if (ExamController.objects.filter(email= request.user)):
			return HttpResponseRedirect('/exam_controller/profile/')
		if (ExamCommitte.objects.filter(email= request.user)):
			return HttpResponseRedirect('/examcommitte/profile/')

