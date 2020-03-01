from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    token = models.CharField(max_length=64,default='')
    class Meta:
        db_table='userinfo'

    def __str__(self):
        return self.username