# Generated by Django 3.2 on 2022-02-10 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('externalcasemanager', '0003_rename_client_assessment_id_externalcmclientintervention_intervention_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='externalcmclientintervention',
            old_name='assessment_date',
            new_name='intervention_date',
        ),
    ]
