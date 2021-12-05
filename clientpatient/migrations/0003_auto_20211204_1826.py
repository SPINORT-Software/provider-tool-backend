# Generated by Django 3.2 on 2021-12-04 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientpatient', '0002_auto_20211122_0433'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personalinformation',
            old_name='language_proficiency_english',
            new_name='language_proficiency',
        ),
        migrations.RemoveField(
            model_name='personalinformation',
            name='language_proficiency_french',
        ),
        migrations.RemoveField(
            model_name='personalinformation',
            name='language_proficiency_interpreter',
        ),
    ]
