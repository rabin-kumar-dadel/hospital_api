# Generated by Django 5.2 on 2025-07-04 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_doctorprofile_experience_years_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='full_name',
            field=models.CharField(default='None', max_length=50),
        ),
    ]
