from django.db import models
import datetime
from datetime import date
today = date.today()


# Create your models he
class Feed(models.Model):
    Uid = models.CharField(max_length = 20,default = '0')
    Date = models.CharField(max_length=20, default=today)
    Feedbacks = models.IntegerField(default = 0)
    Expiry = models.CharField(max_length=20, default='0')
    
    def __str__(self): 
        return self.Uid

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Feed'
        verbose_name_plural = 'Feeds'