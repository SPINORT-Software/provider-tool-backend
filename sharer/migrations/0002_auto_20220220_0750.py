# Generated by Django 3.2 on 2022-02-20 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharercommunication',
            name='discussion_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sharercommunication',
            name='mode_of_communication',
            field=models.CharField(blank=True, choices=[('0', 'Dashboard'), ('1', 'Email'), ('2', 'Fax'), ('3', 'In Person'), ('4', 'Telephone'), ('5', 'Text Message'), ('6', 'Video Conference'), ('7', 'Other')], default='0', max_length=50, null=True),
        ),
    ]
