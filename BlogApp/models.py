from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class BlogPosts(models.Model):
    title = models.CharField(
        max_length=500,
        blank=False,
        null=False,
        unique=True
    )
    tagline = models.CharField(
        max_length=850,
        blank=False,
        null=False
    )
    content = RichTextField()
    thumbnail = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/BlogThumnails'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post_date = models.DateField(
        auto_now_add=True
    )
    category = models.CharField(
        max_length=255,
        default='Coding',
        null=False,
        blank=False
    )
    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name='post_likes'
    )
    
    def __str__(self):
        return f'{self.title} - {self.author.username}'
    
    def total_likes(self):
        return self.likes.count()
    
class Category(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f'{self.name} - {self.added_by.username}'
    
class Service(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return f'{self.name} | {self.added_by} | {self.added_at}'
    
    
class Contact(models.Model):
    name = models.CharField(
        max_length = 255,
        null=False,
        blank=False
    )
    subject = models.CharField(
        max_length=500,
        null=False,
        blank=False
    )
    email = models.EmailField(
        blank=False,
        null=False
    )
    message = models.TextField(
        null=False,
        blank=False
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} | {self.subject} | {self.submitted_at}'

class Newsletter(models.Model):
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'
    
class Quotation(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    email = models.EmailField(
        null=False,
        blank=False
    )
    service = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    message = models.TextField(
        null=False,
        blank=False
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} | {self.service} | {self.submitted_at}'