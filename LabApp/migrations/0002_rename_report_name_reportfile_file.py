# Generated by Django 5.0.1 on 2024-06-15 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LabApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportfile',
            old_name='report_name',
            new_name='file',
        ),
    ]
