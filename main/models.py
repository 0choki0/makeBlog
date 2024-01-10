from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField
from django.conf import settings
from accounts import models as accounts_model

# Create your models here.
class Category(models.Model):
    owner = models.ForeignKey(accounts_model.Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('main:main')

class Post(models.Model):
    category = models.CharField(max_length=20, default="기본 카테고리")
    TAG_CHOICES = [
        ('RESTAURANT', '맛집'),
        ('HOBBY', '취미'),
    ]
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = ResizedImageField(
        size = [500, 500],
        crop = ['middle', 'center'],
        upload_to = 'image/%Y/%m',
    )
    tag = models.CharField(max_length=30, choices = TAG_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title