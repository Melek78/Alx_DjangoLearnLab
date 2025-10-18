from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique= True)
    bio = models.TextField(blank= True, null= True)
    # profile_picture = models.ImageField(upload_to= 'porfile_pics', blank= True, null= True)
    followers = models.ManyToManyField('self', symmetrical= False, related_name= 'followings', blank= True)
    following = models.ManyToManyField('self', symmetrical= False, related_name= 'follower', blank= True)

    def __str__(self):
        return self.username

