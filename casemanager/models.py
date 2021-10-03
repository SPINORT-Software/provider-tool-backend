from django.db import models
import uuid
from clientpatient.models import Client
from django.utils.translation import gettext_lazy as _
from users.models import Users


class CaseManagerUsers(models.Model):
    """
    Case Manager Entity.
    """
    casemanager_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        verbose_name="User - Case Manager",
        db_column="user_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Case Manager"
        verbose_name_plural = "Case Managers"

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"


class ClientStatusChoices(models.TextChoices):
    EXISTING_EMC_NO_REASSESS = 'EXISTING_EMC_NO_REASSESS', _('Existing Extra-Mural Client - No Reassessment')
    EXISTING_EMC_REASSESS = 'EXISTING_EMC_REASSESS', _('Existing Extra-Mural Client Reassessment')
    NEW_EXTRA_MURAL_CLIENT = 'NEW_EXTRA_MURAL_CLIENT', _('New Extra-Mural Client Assessment')
    EXISTING_CASE_CLIENT_REASSESS = 'EXISTING_CASE_CLIENT_REASSESS', _('Existing Case Management Client Reassessment')


class DailyWorkLoad(models.Model):
    daily_workload_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    casemanager = models.ForeignKey(
        CaseManagerUsers,
        on_delete=models.PROTECT,
        verbose_name="Case Manager",
        db_column="casemanager"
    )

    daily_workload_date = models.DateField(null=True, blank=True)
    client_caseload_casemanagement_number_clients = models.IntegerField(null=True, blank=True)
    client_caseload_casemanagement_total_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)

    client_caseload_regular_number_clients = models.IntegerField(null=True, blank=True)
    client_caseload_regular_total_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)

    project_case_management_total_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    project_case_management_admin_total_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    project_case_management_admin_other = models.TextField(blank=True)

    research_related_meetings_total_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    research_related_administration_total_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    research_related_other = models.TextField(blank=True)

    service_recipient_travel = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    functional_center = models.TimeField(auto_now=False, auto_now_add=False, blank=True)

    class Meta:
        verbose_name = 'Daily Workload'
        verbose_name_plural = 'Daily Workloads'

    def __str__(self):
        return self.daily_workload_date


class ExistingEMCAssessment(models.Model):
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)


class NewEMCAssessment(models.Model):
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    total_time = models.TimeField(auto_now=False, auto_now_add=False)
    mode_of_assessment = models.TextField()


class ClientReAssessment(models.Model):
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    reason = models.TextField()
    total_time = models.TimeField(auto_now=False, auto_now_add=False)
    mode_of_assessment = models.TextField()


class ClientAssessment(models.Model):
    client_assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    casemanager = models.ForeignKey(
        CaseManagerUsers,
        on_delete=models.PROTECT,
        verbose_name="Case Manager",
        db_column="casemanager"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Assessment Client",
        db_column="client"
    )
    client_status = models.CharField(
        max_length=100,
        choices=ClientStatusChoices.choices,
        default=ClientStatusChoices.EXISTING_EMC_NO_REASSESS,
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


class ClientIntervention(models.Model):
    intervention_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Intervention Client",
        db_column="client"
    )
    date = models.DateTimeField(null=True, blank=True)
    total_time = models.TimeField(auto_now=False, auto_now_add=False)
    mode_of_intervention = models.TextField()
    clinical_type = models.TextField()
    therapeutic_type = models.TextField()
