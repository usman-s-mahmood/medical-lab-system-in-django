from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.ReportFile)
admin.site.register(models.UploadedFile)
admin.site.register(models.PatientReport)
admin.site.register(models.SampleGeneration)