from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Video(models.Model):
    name=models.CharField(max_length=200)
    video=models.FileField(upload_to="videos")
    tags=models.CharField(max_length=100)



class Comments(models.Model):
    video=models.ForeignKey(Video,related_name='comments',on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.CharField(max_length=100)
