from django.db import models

# Create your models here.
class External_teacher_marks(models.Model):
    student_id = models.CharField(max_length= 150)
    course_code = models.CharField(max_length= 150)
    marks = models.FloatField()
    remarks = models.CharField(max_length= 150)
    session = models.CharField(max_length= 150)

class Send_To_Third_Examinner(models.Model):
    student_id = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    session = models.CharField(max_length=100)

class Third_Examinner_Marks(models.Model):
    student_id = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
    marks = models.FloatField()

class Third_Examinner_ResearchProject_Marks(models.Model):
    student_id = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
    marks = models.FloatField()

class External_Teacher_Research_Project_Marks(models.Model):
    student_id = models.CharField(max_length=200)
    student_name = models.CharField(max_length=200)
    session = models.CharField(max_length=200)
    semester_no = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    credit = models.FloatField()
    remarks = models.CharField(max_length=200)
    supervisor_marks = models.FloatField()
    defence_marks = models.FloatField()
    total_mark = models.FloatField()

class Final_MarkSheet_Theory_Course(models.Model):
    student_id = models.CharField(max_length=200)
    student_name = models.CharField(max_length=200)
    session = models.CharField(max_length=200)
    semester_no = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200)
    credits = models.FloatField()
    remarks = models.CharField(max_length=200)
    hall = models.CharField(max_length=200)
    ct_marks = models.FloatField()
    attendence_mark = models.FloatField()
    total_marks = models.FloatField()
    GP = models.FloatField()
    PS = models.FloatField()
    LG = models.CharField(max_length= 10)

class Final_MarkSheet_ResearchProject_Course(models.Model):
    student_id = models.CharField(max_length=200)
    student_name = models.CharField(max_length=200)
    session = models.CharField(max_length=200)
    semester_no = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200)
    credits = models.FloatField()
    remarks = models.CharField(max_length=200)
    hall = models.CharField(max_length=200)
    total_marks = models.FloatField()
    GP = models.FloatField()
    PS = models.FloatField()
    LG = models.CharField(max_length= 10)