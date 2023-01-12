from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    image = models.ImageField(null=True,blank=True,default='placeholder.png')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.IntegerField(max_length=5, null=True)
    
    def __str__(self):
        return self.title
