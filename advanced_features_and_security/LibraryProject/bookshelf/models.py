from django.db import models
from django.contrib.auth.models import AbstractUser
class Book(models.Model):
    title = models.CharField(max_length= 200)
    author = models.CharField(max_length= 100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author}"

class CustomUser(Abstractuser):
    date_of_birth = models.DateField(null= True, blank= True)
    profile_photo = models.ImageField( null=True, blank=True)