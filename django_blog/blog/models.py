from django.db import models
from django.contrib.auth.models import User
from django.conf import Settings, settings
from django.dispatch import receiver
from django.db.models.signals import post_save

class Post(models.Model):
    title = models.CharField(max_length= 200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add= True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'posts')

    def __str__(self):
        return f"{self.title}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank= True)
    profile_picture = models.ImageField(upload_to= 'profile_pics/', blank= True, null= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.user.username}"
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()