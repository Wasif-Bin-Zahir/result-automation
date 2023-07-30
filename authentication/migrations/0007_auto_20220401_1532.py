# Generated by Django 3.2.9 on 2022-04-01 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_officestuff'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ResearchField',
        ),
        migrations.AddField(
            model_name='officestuff',
            name='user_type',
            field=models.CharField(default='stuff', max_length=100),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user_type',
            field=models.CharField(default='teacher', max_length=100),
        ),
    ]
