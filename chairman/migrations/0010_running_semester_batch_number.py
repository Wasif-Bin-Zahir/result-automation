# Generated by Django 3.2.9 on 2022-04-11 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0009_rename_course_code_registration_by_semester_semester_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='running_semester',
            name='batch_number',
            field=models.IntegerField(default=1),
        ),
    ]
