# Generated by Django 3.2.9 on 2022-04-17 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='External_teacher_marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=150)),
                ('course_code', models.CharField(max_length=150)),
                ('marks', models.FloatField()),
                ('remarks', models.CharField(max_length=150)),
                ('session', models.CharField(max_length=150)),
            ],
        ),
    ]
