# Generated by Django 3.2 on 2022-03-02 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_auto_20220225_0330'),
        ('sharer', '0007_activitynotificationsread_notification-appuser-constraint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitynotificationsread',
            name='application_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications_read', to='authentication.applicationuser'),
        ),
        migrations.AlterField(
            model_name='activitynotificationsread',
            name='notification_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_read', to='sharer.activitynotifications'),
        ),
    ]
