from django.db import models

# Create your models here.

class AdminUser(models.Model):
    image_url = models.URLField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    user_type = models.CharField(max_length=100,default="Super Admin")

    def __str__(self):
        return self.name
    

