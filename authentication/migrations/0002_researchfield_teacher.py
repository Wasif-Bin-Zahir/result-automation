# Generated by Django 3.2.9 on 2022-03-31 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.user')),
                ('profile_img', models.ImageField(upload_to='profileImage')),
                ('position', models.CharField(max_length=100)),
                ('interested_field', models.CharField(max_length=1500)),
            ],
            options={
                'abstract': False,
            },
            bases=('authentication.user',),
        ),
    ]
