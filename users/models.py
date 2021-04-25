from django.db import models

# Create your models here.
from datetime import datetime

from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=32)


class LeastLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loginTime = models.DateTimeField(default=datetime.now(), null=True, blank=True, verbose_name='最近一次登录时间')


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img_url = models.ImageField(upload_to='')
    uploadTime = models.DateTimeField(default=datetime.now())


class DetectImage(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    detectImg_url = models.ImageField(upload_to='')
    detectText_url = models.FileField(upload_to="")
