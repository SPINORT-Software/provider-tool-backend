# Generated by Django 3.2 on 2021-09-15 03:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeValues',
            fields=[
                ('value_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('value_int', models.IntegerField()),
                ('value_decimal', models.DecimalField(decimal_places=4, max_digits=9)),
                ('value_time', models.TimeField()),
                ('value_date', models.DateField()),
                ('value_text', models.TextField()),
                ('attribute', models.ForeignKey(db_column='attribute', on_delete=django.db.models.deletion.PROTECT, to='entities.userroleattribute', verbose_name='role entity attribute')),
                ('entity_data_id', models.ForeignKey(db_column='entity_data_id', on_delete=django.db.models.deletion.CASCADE, to='entities.userroleentitydata', verbose_name='role entity data')),
            ],
        ),
        migrations.AlterField(
            model_name='rolepermissions',
            name='operation_type',
            field=models.CharField(choices=[('CREATE', 'Create'), ('EDIT', 'Edit'), ('DELETE', 'Delete'), ('VIEW', 'View')], default='CREATE', max_length=10, verbose_name='Operation'),
        ),
        migrations.DeleteModel(
            name='UserRoleAttributeValues',
        ),
    ]
