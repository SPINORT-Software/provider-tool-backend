# Generated by Django 3.2 on 2021-08-23 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0003_auto_20210823_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userroleattribute',
            name='attribute_code',
            field=models.CharField(max_length=55, unique=True),
        ),
    ]