# Generated by Django 3.2.9 on 2022-04-16 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('examcontroller', '0002_delete_exteranal_teacher_course'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('authentication', '0012_external_teacher_university_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='External_Teacher',
        ),
    ]
