# Generated by Django 3.2 on 2021-10-02 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('casemanager', '0008_auto_20211002_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientassessment',
            name='existing_assessment',
            field=models.ForeignKey(blank=True, db_column='existing_emp_assessment', on_delete=django.db.models.deletion.PROTECT, to='casemanager.existingemcassessment', verbose_name='Client Assessment'),
        ),
        migrations.AlterField(
            model_name='clientassessment',
            name='newextramuralclient_assessment',
            field=models.ForeignKey(blank=True, db_column='new_extra_muralclient_assessment', on_delete=django.db.models.deletion.PROTECT, to='casemanager.newemcassessment', verbose_name='New Extra-Mural Client Assessment'),
        ),
        migrations.AlterField(
            model_name='clientassessment',
            name='reassessment',
            field=models.ForeignKey(blank=True, db_column='client_reassessment', on_delete=django.db.models.deletion.PROTECT, to='casemanager.clientreassessment', verbose_name='Client Reassessment'),
        ),
    ]
