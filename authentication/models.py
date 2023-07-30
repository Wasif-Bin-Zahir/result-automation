from multiprocessing import managers
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# user managers
class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None, password2=None):
        """
        Creates and saves a User with the given email, name tc and password of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name= name,
            tc= tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  email, name, tc, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# custom user model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length= 200)
    first_name = models.CharField(max_length= 200, default="Unknown")
    last_name = models.CharField(max_length= 200, default="User")
    tc = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


session_list = (
    ('2012-13','2012-13'),
    ('2013-14','2013-14'),
    ('2014-15','2014-15'),
    ('2015-16','2015-16'),
    ('2016-17','2016-17'),
    ('2017-18','2017-18'),
    ('2018-19','2018-19'),
    ('2019-20','2019-20'),
    ('2020-21','2020-21'),
)
hall_name = (
    ('JAMH', 'JAMH'),
    ('BSMRH', 'BSMRH'),
    ('SRH', 'SRH'),
    ('AKH', 'AKH'),
    ('BSFH', 'BSFH'),
)

class Student(User):
    session = models.CharField(
        choices= session_list,
        max_length= 100,
        default='2016-17',
    )
    student_id = models.CharField(max_length=10)
    profile_image = models.URLField(default="https://i.ibb.co/S5cx8vv/R-1.jpg") 
    hall = models.CharField(
        max_length= 120,
        choices= hall_name,
        default= 'JAMH',
    )
    user_type = models.CharField(max_length= 100, default="student")


class Teacher(User):
    profile_img = models.URLField(default="https://i.ibb.co/S5cx8vv/R-1.jpg") 
    position = models.CharField(max_length=100)
    interested_field = models.CharField(max_length= 1500)
    mobile_number = models.CharField(max_length=100, default='Not Interested')
    user_type = models.CharField(max_length= 100, default="teacher")

    def __str__(self):
        return self.first_name + " "+ self.last_name

class Teacher_email(models.Model):
    email = models.EmailField(max_length=150, unique=True)

class OfficeStuff(User):
    profile_img = models.URLField(default="https://i.ibb.co/S5cx8vv/R-1.jpg")  
    position = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=100, default='Not Interested')
    user_type = models.CharField(max_length= 100, default="stuff")

class ExamController(User):
    profile_img = models.URLField(default="https://i.ibb.co/S5cx8vv/R-1.jpg")  
    mobile_number = models.CharField(max_length=100, default='Not Interested')
    user_type = models.CharField(max_length= 100, default="exam_controller")

class ExamCommitte(User):
    profile_img = models.URLField(default="https://i.ibb.co/S5cx8vv/R-1.jpg") 
    mobile_number = models.CharField(max_length=100, default='Not Interested')
    user_type = models.CharField(max_length= 100, default="ExamCommitte")
    def __str__(self):
        return self.first_name + " "+ self.last_name
