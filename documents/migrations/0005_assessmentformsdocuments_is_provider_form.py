# Generated by Django 3.2 on 2021-10-02 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_communityparamedicformsdocuments'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentformsdocuments',
            name='is_provider_form',
            field=models.BooleanField(default=False),
        ),
    ]
