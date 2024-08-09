from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False
    )
    about_user = models.CharField(
        max_length=1000,
        null=False
    )
    social_link = models.URLField(null=True)
    profile_pic = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/ProfilePictures'
    )
    
    def __str__(self):
        return (self.user.username)