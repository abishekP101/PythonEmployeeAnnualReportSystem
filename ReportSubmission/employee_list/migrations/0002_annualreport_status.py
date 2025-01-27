# Generated by Django 5.1.4 on 2025-01-15 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='annualreport',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
