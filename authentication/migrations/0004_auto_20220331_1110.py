# Generated by Django 3.2.9 on 2022-03-31 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_teacher_hometown'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='hometown',
        ),
        migrations.AddField(
            model_name='teacher',
            name='mobile_number',
            field=models.CharField(default='Not Interested', max_length=100),
        ),
    ]
