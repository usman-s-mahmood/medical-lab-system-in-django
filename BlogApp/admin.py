from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.BlogPosts)
admin.site.register(models.Service)
admin.site.register(models.Contact)
admin.site.register(models.Newsletter)
admin.site.register(models.Quotation)