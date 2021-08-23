# Generated by Django 3.2 on 2021-08-23 06:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0006_userroleattribute_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='userroleattribute',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userroleattribute',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]