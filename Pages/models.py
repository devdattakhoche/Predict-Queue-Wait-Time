from django.db import models

# x

class Hospital(models.Model):
    Hospital_id = models.IntegerField(primary_key=True,unique=True,null=False,blank=False)
    Hospital_name = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.Hospital_name

class Dept(models.Model):
    class Meta:
        unique_together = (('Uid','Hospital_id'),)

    Uid=models.IntegerField(primary_key=True,unique=True,null=False,blank=False)
    Type = models.CharField(max_length=20,default='')
    image = models.ImageField(upload_to="department_images/",default="")
    Hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE,default=1)
    

    def __str__(self):
        return self.Type 

