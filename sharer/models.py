import datetime
import math

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from rest_framework import serializers
from asgiref.sync import async_to_sync
from django.utils.timesince import timesince as timesince_

import json
import uuid
import logging

from authentication.models import ApplicationUser
from casemanager.models import CaseManagerClientAssessment, ClientIntervention
from clinician.models import ClinicianClientAssessment, ClinicianClientInterventions
from core.constants import WS_CONSUMER_GROUPS
from authentication.serializers import ApplicationUserListSerializer

logger = logging.getLogger(__name__)


class CommunicationModeChoices(models.TextChoices):
    DASHBOARD = 0, _('Dashboard')
    EMAIL = 1, _('Email')
    FAX = 2, _('Fax')
    IN_PERSON = 3, _('In Person')
    TELEPHONE = 4, _('Telephone')
    TEXT_MESSAGE = 5, _('Text Message')
    VIDEO_CONFERENCE = 6, _('Video Conference')
    OTHER = 7, _('Other')


class CommunicationTypeChoices(models.TextChoices):
    INTERNAL_REFERRAL = 0, _('Internal Referral')
    EXTERNAL_REFERRAL = 1, _('External Referral')
    INTERNAL_FOLLOWUP = 2, _('Internal Follow Up')
    EXTERNAL_FOLLOWUP = 3, _('External Follow Up')
    DEFAULT = 4, _('DEFAULT')


class NotificationType(models.TextChoices):
    CREATED = 0, _('CREATED')
    EDITED = 1, _('EDITED')
    DELETED = 2, _('DELETED')
    REFERRED = 3, _('REFERRED')
    FOLLOW_UP = 4, _('FOLLOW_UP')


class FollowUpDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(communication_type__in=[CommunicationTypeChoices.EXTERNAL_FOLLOWUP,
                                                                     CommunicationTypeChoices.INTERNAL_FOLLOWUP])


class ReferralDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(communication_type__in=[CommunicationTypeChoices.INTERNAL_REFERRAL,
                                                                     CommunicationTypeChoices.EXTERNAL_REFERRAL])


class SharerCommunication(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    communication_by = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Communication By",
        related_name="communication_by"
    )
    communication_to = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Communication To",
        related_name="communication_to"
    )
    communication_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    content_type = models.ForeignKey(ContentType, related_name="content_type_communication", on_delete=models.CASCADE)
    object_id = models.UUIDField(default=uuid.uuid4, editable=False)
    communication_object = GenericForeignKey('content_type', 'object_id')

    communication_type = models.CharField(
        max_length=50,
        choices=CommunicationTypeChoices.choices,
        default=CommunicationTypeChoices.DEFAULT
    )
    mode_of_communication = models.CharField(
        max_length=50,
        choices=CommunicationModeChoices.choices,
        default=CommunicationModeChoices.DASHBOARD,
        blank=True,
        null=True
    )

    discussion_details = models.TextField(null=True, blank=True)

    followups = FollowUpDataManager()
    referrals = ReferralDataManager()
    objects = models.Manager()

    def __str__(self):
        return self.communication_type


class ActivityNotifications(models.Model):
    notification_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    action_object_content_type = models.ForeignKey(ContentType, related_name="notification_action_object",
                                                   on_delete=models.CASCADE)
    action_object_object_id = models.UUIDField(default=uuid.uuid4, editable=False)
    action_object = GenericForeignKey('action_object_content_type', 'action_object_object_id')
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        default=NotificationType.CREATED
    )
    notification_sent_by = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Notification By",
        related_name="notification_by"
    )

    class Meta:
        ordering = ('-timestamp',)

    @property
    def timesince(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = now - self.timestamp
        total_seconds_ago = delta.total_seconds()
        total_minutes_ago = total_seconds_ago / 60

        if 60 < total_minutes_ago < 1440:
            return f"{math.floor(total_minutes_ago / 60)} hours ago"

        if total_minutes_ago > 1440:
            return f"{math.floor((total_minutes_ago / 60) / 24)} days ago"

        if total_minutes_ago < 60:
            return f"{math.floor(total_minutes_ago)} minutes ago"

    def __str__(self):
        return f"{str(self.action_object_content_type)} - {self.get_notification_type_display()} - {str(self.timestamp.date())} {str(self.timestamp.time())}"

    def save(self, *args, **kwargs):
        logger.info("Save method called")
        super(ActivityNotifications, self).save(*args, **kwargs)


class ActivityNotificationsRead(models.Model):
    notification_id = models.ForeignKey(ActivityNotifications, on_delete=models.CASCADE,
                                        related_name="notifications_read")
    application_user = models.ForeignKey(ApplicationUser, related_name='user_notifications_read',
                                         on_delete=models.CASCADE)
    last_read_time = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['notification_id', 'application_user'],
                                    name='Notification-AppUser-Constraint')
        ]


class NotificationDataSerializer(serializers.Serializer):
    by = serializers.SerializerMethodField('get_application_user_detail')
    type = serializers.SerializerMethodField('get_notification_type')
    id = serializers.SerializerMethodField('get_notification_id')
    ts = serializers.SerializerMethodField('get_timestamp')
    otype = serializers.SerializerMethodField('get_object_type')
    otype_code = serializers.SerializerMethodField('get_object_type_code')
    o = serializers.SerializerMethodField('get_object_pk')
    timesince = serializers.SerializerMethodField('get_timesince')

    def get_application_user_detail(self, object):
        return ApplicationUserListSerializer(object.notification_sent_by).data

    def get_notification_id(self, object):
        return str(object.notification_id)

    def get_notification_type(self, object):
        return object.get_notification_type_display()

    def get_timestamp(self, object):
        return object.timestamp.strftime("%m/%d/%Y, %H:%M:%S")

    def get_object_type(self, object):
        return object.action_object_content_type.model_class()._meta.verbose_name.title()

    def get_object_type_code(self, object):
        return object.action_object_content_type.model_class().__name__

    def get_object_pk(self, object):
        return str(object.action_object.pk)

    def get_timesince(self, object):
        return str(object.timesince)


def send_to_channel_layer(notification: ActivityNotifications):
    channel_layer = get_channel_layer()
    serialized_data = NotificationDataSerializer(notification).data

    data = {
        'type': 'send_notification',
        'value': serialized_data
    }
    async_to_sync(channel_layer.group_send)(WS_CONSUMER_GROUPS.get("NOTIFICATIONS"), data)


@receiver(post_save, sender=CaseManagerClientAssessment)
def create_activitynotifications_casemanager_clientassessment(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Adding notification for {instance}")
        notification = ActivityNotifications.objects.create(notification_type=NotificationType.CREATED,
                                                            notification_sent_by=instance.casemanager,
                                                            action_object=instance)
        send_to_channel_layer(notification)


@receiver(post_save, sender=ClientIntervention)
def create_activitynotifications_casemanager_clientintervention(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Adding notification for {instance}")
        notification = ActivityNotifications.objects.create(notification_type=NotificationType.CREATED,
                                                            notification_sent_by=instance.casemanager,
                                                            action_object=instance)
        send_to_channel_layer(notification)


@receiver(post_save, sender=ClinicianClientAssessment)
def create_activitynotifications_casemanager_clientassessment(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Adding notification for {instance}")
        notification = ActivityNotifications.objects.create(notification_type=NotificationType.CREATED,
                                                            notification_sent_by=instance.clinician,
                                                            action_object=instance)

        send_to_channel_layer(notification)


@receiver(post_save, sender=ClinicianClientInterventions)
def create_activitynotifications_casemanager_clientintervention(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Adding notification for {instance}")
        notification = ActivityNotifications.objects.create(notification_type=NotificationType.CREATED,
                                                            notification_sent_by=instance.clinician,
                                                            action_object=instance)

        send_to_channel_layer(notification)
