# Generated by Django 3.2 on 2022-02-21 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharer', '0002_auto_20220220_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharercommunication',
            name='communication_type',
            field=models.CharField(choices=[('0', 'Internal Referral'), ('1', 'External Referral'), ('2', 'Internal Follow Up'), ('3', 'External Follow Up'), ('4', 'DEFAULT')], default='4', max_length=50),
        ),
    ]
