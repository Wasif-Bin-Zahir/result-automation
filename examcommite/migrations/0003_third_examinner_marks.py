# Generated by Django 3.2.9 on 2022-04-18 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examcommite', '0002_send_to_third_examinner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Third_Examinner_Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=100)),
                ('course_code', models.CharField(max_length=100)),
                ('session', models.CharField(max_length=100)),
                ('marks', models.FloatField()),
            ],
        ),
    ]