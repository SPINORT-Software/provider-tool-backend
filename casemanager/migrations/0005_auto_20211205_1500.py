# Generated by Django 3.2 on 2021-12-05 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casemanager', '0004_alter_casemanagerusers_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyworkload',
            name='client_caseload_casemanagement_total_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='client_caseload_regular_total_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='functional_center',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='project_case_management_admin_total_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='project_case_management_total_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='research_related_administration_total_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='research_related_meetings_total_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='research_related_other',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='service_recipient_travel',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
