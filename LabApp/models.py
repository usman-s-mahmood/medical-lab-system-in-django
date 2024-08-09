from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class ReportFile(models.Model):
    file = models.FileField(
        null=False,
        blank=False,
        upload_to='reports/clients'
    )
    owner_name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    owner_email = models.EmailField(
        null=False,
        blank=False,
        unique=False
    )
    report_type = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True        
    )
    
    def __str__(self):
        return f'ID: {self.pk} | {self.owner_name} - {self.report_type}'
    
class UploadedFile(models.Model):
    upload_name = models.FileField(
        upload_to='reports/uploads',
        null=False,
        blank=False
    )
    file_category = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True        
    )
    
    def __str__(self):
        return f'ID: {self.pk} | {self.file_category}'
    
class PatientReport(models.Model):
    patient_name = models.CharField(
        max_length=500,
        null=False,
        blank=False
    )
    phone_number = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    patient_email = models.EmailField(
        null=False,
        blank=False
    )
    test_type = models.CharField(
        max_length=500,
        null=False,
        blank=False
    )
    result = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    evaluation = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    filename = models.TextField(
        null=False,
        blank=False
    )
    payment = models.FloatField(
        default=0.0,
        null=False,
        blank=False
    )
    payment_status = models.CharField(
        max_length = 50,
        default = 'unpaid',
        null=False,
        blank=False
    )
    date_of_birth = models.DateTimeField(
        default=date(2000, 1, 1),
        null=False,
        blank=False
    )
    age = models.IntegerField(
        default=18,
        null=False,
        blank=False
    )
    
    
    def __str__(self):
        return f'ID: {self.id} | {self.patient_name} | {self.test_type} | {self.evaluation} '
    
class SampleGeneration(models.Model):
    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    record_size = models.IntegerField(
        null=False,
        blank=False
    )
    filename = models.CharField(
        max_length=11550,
        null=False,
        blank=False
    )
    
    def __str__(self):
        return f'ID: {self.pk} | Generated By: {self.generated_by.username}'