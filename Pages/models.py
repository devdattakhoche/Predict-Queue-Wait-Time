from django.db import models

# Create your models here.
class Dept(models.Model):
    Uid=models.IntegerField(primary_key=True,unique=True,null=False,blank=False)
    Type = models.CharField(max_length=20,default='')
    image = models.ImageField(upload_to="department_images/",default="")
    

    def __str__(self):
        return self.Type 
