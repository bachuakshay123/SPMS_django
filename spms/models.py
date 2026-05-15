from django.db import models
class login (models.Model):
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    mobile_number=models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.username