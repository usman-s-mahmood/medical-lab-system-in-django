# Generated by Django 5.0.1 on 2024-06-03 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0005_contact_newsletter_quotation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotation',
            name='phone_number',
        ),
    ]