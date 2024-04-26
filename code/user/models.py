from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CustomUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=20,unique=True,blank=False,primary_key=True)
    validation_code=models.CharField(max_length=10,blank=False)
    REQUIRED_FIELDS = ["phone", "validation_code"]
    
    def __str__(self) -> str:
        return 'CustomUser %s'%(self.phone)