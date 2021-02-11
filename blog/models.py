from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    image=models.ImageField(upload_to='images/')
    author=models.ForeignKey(User,related_name='blog_post',on_delete=models.CASCADE)
    body=models.TextField(default='')
    public=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

