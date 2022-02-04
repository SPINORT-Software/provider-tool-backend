from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import uuid

from authentication.models import Types as UserTypes, ApplicationUser
from core.models import *
from clientpatient.models import Client
from core.models import ProviderTypes

class DailyWorkLoad(models.Model):
    daily_workload_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    clinician = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Clinician",
        db_column="clinician",
        related_name="clinician_dailyworkload"
    )
    daily_workload_date = models.TextField(null=True, blank=True)

    client_caseload_casemanagement_number_clients = models.TextField(null=True, blank=True)
    client_caseload_casemanagement_total_time = models.TextField(null=True, blank=True)
    client_caseload_regular_number_clients = models.TextField(null=True, blank=True)
    client_caseload_regular_total_time = models.TextField(null=True, blank=True)

    service_recipient_travel = models.TextField(null=True, blank=True)
    functional_center = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Daily Workload'
        verbose_name_plural = 'Daily Workloads'

    def __str__(self):
        return self.daily_workload_date


class ClinicianClientAssessment(models.Model):
    client_assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    clinician = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Clinician",
        db_column="clinician",
        related_name="clinician_clientassessment"
    )
    client = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Clinician Assessment Client",
        db_column="clinician_client",
        related_name="clinician_client"
    )
    assessment_status = models.CharField(
        max_length=100,
        choices=ClientStatusChoices.choices,
        default=ClientStatusChoices.NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS,
        blank=True
    )
    existing_assessment = models.ForeignKey(
        ExistingEMCAssessment,
        on_delete=models.PROTECT,
        verbose_name="Existing Extra Mural Client Assessment",
        db_column="existing_emp_assessment",
        null=True,
        blank=True
    )
    reassessment = models.ForeignKey(
        ClientReAssessment,
        on_delete=models.PROTECT,
        verbose_name="Client Reassessment",
        db_column="client_reassessment",
        null=True,
        blank=True
    )
    newextramuralclient_assessment = models.ForeignKey(
        NewEMCAssessment,
        on_delete=models.PROTECT,
        verbose_name="New Extra-Mural Client Assessment",
        db_column="new_extra_muralclient_assessment",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Client Assessment"
        verbose_name_plural = "Client Assessments"

    def __str__(self):
        return self.client_status + " [" + str(self.client_assessment_id) + "]"


class ClinicianClientInterventions(models.Model):
    intervention_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Clinician Intervention Client",
        db_column="client",
        related_name="clinician_intervention_client"
    )
    clinician = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Clinician",
        db_column="clinician",
        related_name="clinician_intervention_clinician"
    )
    date = models.DateField(null=True, blank=True)
    total_time = models.TimeField(auto_now=False, auto_now_add=False)
    mode_of_clinical_intervention = models.JSONField(null=True, blank=True)
    clinical_type = models.JSONField(null=True, blank=True)
    clinical_type_detail = models.TextField(null=True, blank=True)
    therapeutic_type = models.JSONField(null=True, blank=True)
    therapeutic_type_detail = models.TextField(null=True, blank=True)


# class ClinicanUsers(models.Model):
#     """
#     Clinician Entity.
#     """
#     clinician_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         verbose_name="User - Clinican",
#         db_column="user_id",
#         related_name="clinicianuser"
#     )
#     provider_type = models.CharField(
#         max_length=100,
#         choices=ProviderTypes.choices,
#         default=ProviderTypes.PROVIDER_TYPE_DEFAULT,
#         null=True,
#         blank=True
#     )
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#
#     class Meta:
#         verbose_name = "Clinican"
#         verbose_name_plural = "Clinicans"
#
#     def __str__(self):
#         return f"{self.user.first_name} {self.user.last_name}"


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_clinicianusers(sender, instance, created, **kwargs):
#     if created:
#         if hasattr(instance, 'user_type') and instance.user_type == UserTypes.TYPE_CLINICIAN:
#             ClinicanUsers.objects.create(user=instance)
