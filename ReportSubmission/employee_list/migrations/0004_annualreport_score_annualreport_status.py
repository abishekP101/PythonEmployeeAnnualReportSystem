# Generated by Django 5.1.4 on 2025-01-15 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_list', '0003_remove_annualreport_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='annualreport',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='annualreport',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('viewed', 'Viewed')], default='pending', max_length=10),
        ),
    ]
