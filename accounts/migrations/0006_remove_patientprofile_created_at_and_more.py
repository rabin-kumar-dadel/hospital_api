# Generated by Django 5.2 on 2025-07-03 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_patientprofile_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientprofile',
            name='created_at',
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='date_of_birth',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='district',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default=None, max_length=10),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='lastname',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='local_level',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='middle_name',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='phone',
            field=models.CharField(default=None, max_length=15),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='province',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='street_address',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='ward_number',
            field=models.CharField(default=None, max_length=10),
        ),
    ]
