# Generated by Django 3.2 on 2021-08-23 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_userroleattribute_attribute_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='userroleattribute',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]