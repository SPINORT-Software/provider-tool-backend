# Generated by Django 3.2 on 2021-08-23 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userroleentitydatatypes',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
