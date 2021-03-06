# Generated by Django 3.2 on 2021-04-22 14:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='LeastLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loginTime', models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 22, 14, 56, 21, 587627), null=True, verbose_name='最近一次登录时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.ImageField(upload_to='')),
                ('uploadTime', models.DateTimeField(default=datetime.datetime(2021, 4, 22, 14, 56, 21, 587627))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='DetectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detectImg_url', models.ImageField(upload_to='')),
                ('detectText_url', models.FileField(upload_to='')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.image')),
            ],
        ),
    ]
