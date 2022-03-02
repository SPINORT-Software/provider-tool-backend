from django.db import models
import uuid
# from clientpatient.models import Client
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
from authentication.models import Types as UserTypes, ApplicationUser
from core.models import *
import logging


logger = logging.getLogger(__name__)

class DailyWorkLoad(models.Model):
    daily_workload_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    casemanager = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Case Manager",
        db_column="casemanager"
    )
    daily_workload_date = models.DateField(null=True, blank=True)
    client_caseload_casemanagement_number_clients = models.TextField(null=True, blank=True)
    client_caseload_casemanagement_total_time = models.TextField(null=True, blank=True)

    client_caseload_regular_number_clients = models.TextField(null=True, blank=True)
    client_caseload_regular_total_time = models.TextField(null=True, blank=True)

    project_case_management_total_time = models.TextField(null=True, blank=True)
    project_case_management_admin_total_time = models.TextField(null=True, blank=True)
    project_case_management_admin_other = models.TextField(null=True, blank=True)

    research_related_meetings_total_time = models.TextField(null=True, blank=True)
    research_related_administration_total_time = models.TextField(null=True, blank=True)
    research_related_other = models.TextField(null=True, blank=True)

    service_recipient_travel = models.TextField(null=True, blank=True)
    functional_center = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Daily Workload'
        verbose_name_plural = 'Daily Workloads'

    def __str__(self):
        return f"{self.casemanager.user.first_name} : {str(self.daily_workload_date)}"


class CaseManagerClientAssessment(models.Model):
    client_assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    assessment_date = models.DateField(auto_now_add=True, null=True, blank=True)
    assessment_time = models.TimeField(auto_now_add=True, null=True, blank=True)
    casemanager = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Case Manager",
        db_column="casemanager",
        related_name="clientassessment_casemanager"
    )
    client = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Assessment Client",
        db_column="client",
        related_name="clientassessment_client"
    )
    assessment_status = models.CharField(
        max_length=100,
        choices=ClientStatusChoices.choices,
        default=ClientStatusChoices.NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS,
        blank=True,
        db_column="assessment_status"
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
        return self.assessment_status + " [" + str(self.client_assessment_id) + "]"


class ClientIntervention(models.Model):
    intervention_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Intervention Client",
        db_column="client",
        related_name='clientintervention_client'
    )
    casemanager = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Client Intervention Case Manager",
        db_column="client_intervention_casemanager",
        related_name='clientintervention_casemanager'
    )
    date = models.TextField(null=True, blank=True)
    total_time = models.TextField(null=True, blank=True)
    mode_of_clinical_intervention = models.JSONField(null=True, blank=True)
    clinical_type = models.JSONField(null=True, blank=True)
    clinical_type_detail = models.TextField(null=True, blank=True)
    therapeutic_type = models.JSONField(null=True, blank=True)
    therapeutic_type_detail = models.TextField(null=True, blank=True)




# class CaseManagerUsers(models.Model):
#     """
#     Case Manager Entity.
#     """
#     casemanager_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         verbose_name="User - Case Manager",
#         db_column="user_id",
#         related_name="casemanager"
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     provider_type = models.CharField(
#         max_length=100,
#         choices=ProviderTypes.choices,
#         default=ProviderTypes.PROVIDER_TYPE_DEFAULT,
#         null=True,
#         blank=True
#     )
#
#     class Meta:
#         verbose_name = "Case Manager"
#         verbose_name_plural = "Case Managers"
#
#     def __str__(self):
#         return f"{self.user.first_name} {self.user.last_name}"


