# Generated by Django 5.0.6 on 2024-06-24 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LabApp', '0007_patientreport_age_patientreport_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientreport',
            name='payment_status',
            field=models.CharField(default='unpaid', max_length=50),
        ),
    ]