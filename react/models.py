from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    type_of = models.CharField(max_length=15,default='Image',choices=[("0","Customer"),("1","Admin"),])
    email = models.EmailField(unique=True,max_length=255)
    username = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'user'