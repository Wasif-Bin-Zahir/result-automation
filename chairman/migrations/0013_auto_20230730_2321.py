# Generated by Django 3.2.9 on 2023-07-30 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0012_alter_course_course_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Show_By_Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=150)),
                ('student_id', models.CharField(max_length=150)),
            ],
        ),
        migrations.AlterField(
            model_name='running_semester',
            name='session',
            field=models.CharField(choices=[('2017-18', '2017-18'), ('2018-19', '2018-19'), ('2019-20', '2019-20'), ('2020-21', '2020-21'), ('2021-22', '2021-22')], default='2016-17', max_length=100),
        ),
    ]
