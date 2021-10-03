# Generated by Django 3.2 on 2021-09-30 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_referralformsdocuments'),
        ('reviewboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralformsdocuments',
            name='client_referral',
            field=models.ForeignKey(db_column='client_referral', on_delete=django.db.models.deletion.PROTECT, to='reviewboard.clientreferral', verbose_name='Client Referral'),
        ),
        migrations.AddField(
            model_name='referralformsdocuments',
            name='document',
            field=models.ForeignKey(db_column='document', on_delete=django.db.models.deletion.PROTECT, to='documents.documents', verbose_name='Document'),
        ),
    ]
