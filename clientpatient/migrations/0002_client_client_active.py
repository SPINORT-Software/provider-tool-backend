# Generated by Django 3.2 on 2021-09-30 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientpatient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='client_active',
            field=models.BooleanField(default=False),
        ),
    ]
