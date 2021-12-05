# Generated by Django 3.2 on 2021-12-05 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casemanager', '0006_alter_dailyworkload_research_related_other'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyworkload',
            name='client_caseload_casemanagement_number_clients',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='client_caseload_casemanagement_total_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='client_caseload_regular_number_clients',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='client_caseload_regular_total_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='functional_center',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='project_case_management_admin_other',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='project_case_management_admin_total_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='project_case_management_total_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='research_related_administration_total_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='research_related_meetings_total_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='research_related_other',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyworkload',
            name='service_recipient_travel',
            field=models.TextField(blank=True, null=True),
        ),
    ]
