# Generated by Django 3.2 on 2021-11-23 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', 'add_document_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='user',
            field=models.ForeignKey(db_column='user_id', default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]