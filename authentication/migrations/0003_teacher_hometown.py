# Generated by Django 3.2.9 on 2022-03-31 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_researchfield_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='hometown',
            field=models.CharField(default='Dhaka', max_length=100),
        ),
    ]