# Generated by Django 3.2.9 on 2022-04-06 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20220403_1001'),
        ('chairman', '0003_roll_sheet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher_Student_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=200)),
                ('student_id', models.CharField(max_length=200)),
                ('course_name', models.CharField(max_length=200)),
                ('course_code', models.CharField(max_length=200)),
                ('hall', models.CharField(max_length=150)),
                ('session', models.CharField(max_length=120)),
                ('credit', models.FloatField()),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authentication.teacher')),
            ],
        ),
    ]
