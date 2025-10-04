from django.db import models
from django.contrib.auth.models import User
from django.conf import Settings, settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import slugify
from taggit.managers import TaggableManager

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts-by-tag', kwargs={'tag_slug': self.slug})
    
class Post(models.Model):
    title = models.CharField(max_length= 200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add= True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'posts')
    tags = TaggableManager(blank=True)

    def __str__(self):
        return f"{self.title}"
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

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

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.post.pk})

