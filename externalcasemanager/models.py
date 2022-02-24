from django.db import models

import uuid
from authentication.models import ApplicationUser
from core.models import *


class ExternalCMClientIntervention(models.Model):
    intervention_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    created_time = models.TimeField(auto_now_add=True, null=True, blank=True)
    casemanager = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Case Manager",
        db_column="casemanager",
        related_name="external_intervention_casemanager"
    )
    client = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Client",
        db_column="client",
        related_name="external_intervention_client"
    )
    assessment_status = models.CharField(
        max_length=100,
        choices=ExternalPartnerClientStatusChoices.choices,
        default=ExternalPartnerClientStatusChoices.NEW_CASE_MANAGEMENT_CLIENT,
        blank=True,
        db_column="assessment_status"
    )
    intervention_date = models.DateField(auto_now_add=False, null=True, blank=True)
    internal_comm_assessment_clinical_notes = models.TextField(null=True, blank=True)
    internal_comm_followup_clinical_notes = models.TextField(null=True, blank=True)
    internal_comm_internal_referral_notes = models.TextField(null=True, blank=True)


