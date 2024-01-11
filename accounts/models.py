from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# Create your models here.
class User(AbstractUser):
    profile_image = ResizedImageField(
        size = [200, 200],
        crop = ['middle', 'center'],
        upload_to = 'profile',
        default = 'profile/default.png',
    )
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)

class Blog(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.owner.username