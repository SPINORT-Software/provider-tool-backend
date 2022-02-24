from django.db import models
import uuid
from authentication.models import ApplicationUser
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from clinician.models import ClinicianClientAssessment, ClinicianClientInterventions
from casemanager.models import CaseManagerClientAssessment, ClientIntervention

from django.utils import timezone

"""
Internal Referral for Client Assessments, Client Interventions 
"""
COMMUNICATION_OBJECT_INSTANCE_TYPES = {
    1: ClinicianClientAssessment,
    2: CaseManagerClientAssessment,
    3: ClientIntervention,
    4: ClinicianClientInterventions
}



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

    class Meta:
        ordering = ('-timestamp',)

    def timesince(self, now=None):
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.timestamp, now)


class ActivityNotificationsRead(models.Model):
    notification_id = models.ForeignKey(ActivityNotifications, on_delete=models.CASCADE)
    application_user = models.ForeignKey(ApplicationUser, related_name='notifications_read', on_delete=models.CASCADE)
    last_read_time = models.DateTimeField(default=timezone.now, db_index=True)
