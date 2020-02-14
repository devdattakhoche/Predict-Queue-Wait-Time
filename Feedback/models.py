from django.db import models
import datetime
from datetime import date
today = date.today()


# Create your models he
class Feedback(models.Model):
    Uid = models.CharField(max_length = 20)
    Date = models.CharField(max_length=20, default=today)

    def __str__(self): 
        return self.Uid

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'