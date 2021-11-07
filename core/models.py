from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class ExistingEMCAssessment(models.Model):
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)


class NewEMCAssessment(models.Model):
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    total_time = models.TimeField(auto_now=False, auto_now_add=False)
    mode_of_assessment = models.TextField(null=True, blank=True)


class ClientReAssessment(models.Model):
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    total_time = models.TimeField(auto_now=False, auto_now_add=False)
    mode_of_assessment = models.TextField(null=True, blank=True)


class ClientStatusChoices(models.TextChoices):
    NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS = 'NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS', _(
        'Existing Extra-Mural Client - No Reassessment')
    NEW_CASE_CLIENT_EXISTING_EMC_REASSESS = 'NEW_CASE_CLIENT_EXISTING_EMC_REASSESS', _(
        'Existing Extra-Mural Client Reassessment')
    NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT = 'NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT', _(
        'New Extra-Mural Client Assessment')
    EXISTING_CASE_CLIENT_REASSESS = 'EXISTING_CASE_CLIENT_REASSESS', _('Existing Case Management Client Reassessment')
