from django.db import models
from authentication.models import Teacher
# Create your models here.

semister = (
    ('1st Year 1st Semester', '1st Year 1st Semester'),
    ('1st Year 2nd Semester', '1st Year 2nd Semester'),
    ('2nd Year 1st Semester', '2nd Year 1st Semester'),
    ('2nd Year 2nd Semester', '2nd Year 2nd Semester'),
    ('3rd Year 1st Semester', '3rd Year 1st Semester'),
    ('3rd Year 2nd Semester', '3rd Year 2nd Semester'),
    ('4th Year 1st Semester', '4th Year 1st Semester'),
    ('4th Year 2nd Semester', '4th Year 2nd Semester'),
)
course_types = (
    ('Theory', 'Theory'),
    ('Lab', 'Lab'),
    ('Project', 'Project'),
    ('Research_Project', 'Research_Project'),
    ('Viva', 'Viva'),
    ('None', 'None'),
)
session_list = (
   
    ('2017-18','2017-18'),
    ('2018-19','2018-19'),
    ('2019-20','2019-20'),
    ('2020-21','2020-21'),
    ('2021-22','2021-22'),
)

class Course(models.Model):
    course_name = models.CharField(max_length=150)
    course_code = models.CharField(max_length=150)
    course_type = models.CharField(
        max_length=200,
        choices= course_types,
        default= 'Theory'
        )
    credit = models.FloatField()
    semister_no = models.CharField(
        max_length=200,
        choices= semister,
        default= '1st Year 1st Semester'
        )
    course_teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)

    def __str__(self):
        return self.course_name

class Running_Semester(models.Model):
    semester_no = models.CharField(
        max_length=120,
        choices= semister,
        default='1st Year 1st Semester'
    )
    session = models.CharField(
        choices= session_list,
        max_length= 100,
        default='2016-17',
    )
    batch_number = models.IntegerField(default=1)

class Roll_Sheet(models.Model):
    session = models.CharField(max_length=150)
    student_id = models.CharField(max_length=120)
    name_of_student = models.CharField(max_length=150)
    hall = models.CharField(max_length=299)
    course_code = models.CharField(max_length=500)
    remarks = models.CharField(max_length=150)
    semester = models.CharField(
        max_length=120,
        choices= semister,
        default= '3rd Year 1st Semester',
    )

class Teacher_Student_Info(models.Model):
    student_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    hall = models.CharField(max_length=150)
    session = models.CharField(max_length=120)
    credit = models.FloatField()
    remarks = models.CharField(max_length=150, default='Regular')
    semester = models.CharField(
        max_length=120,
        choices= semister,
        default= '3rd Year 1st Semester',
    )

class Registration_By_Semester(models.Model):
    session = models.CharField(max_length=150)
    student_id = models.CharField(max_length=150)
    name_of_the_candidates = models.CharField(max_length=150)
    hall = models.CharField(max_length=160)
    semester_name = models.CharField(max_length=30)
    remarks = models.CharField(max_length=150)

class Show_By_Semester(models.Model):
    session = models.CharField(max_length=150)
    student_id = models.CharField(max_length=150)
   