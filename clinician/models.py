from django.db import models
from django.contrib.auth.models import User
import uuid
from clientpatient.models import Client
from django.utils.translation import gettext_lazy as _


class ClinicanUsers(models.Model):
    """
    Clinician Entity.
    """
    clinician_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="User - Clinican",
        db_column="user_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Clinican"
        verbose_name_plural = "Clinicans"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class DailyWorkLoad(models.Model):
    daily_workload_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    clinician = models.ForeignKey(
        ClinicanUsers,
        on_delete=models.PROTECT,
        verbose_name="Clinician",
        db_column="clinician"
    )
    daily_workload_date = models.DateField(null=True, blank=True)
    client_caseload_casemanagement_number_clients = models.IntegerField(null=True, blank=True)
    client_caseload_casemanagement_total_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    client_caseload_regular_number_clients = models.IntegerField(null=True, blank=True)
    client_caseload_regular_total_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    service_recipient_travel = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    functional_center = models.TimeField(auto_now=False, auto_now_add=False, blank=True)

    class Meta:
        verbose_name = 'Daily Workload'
        verbose_name_plural = 'Daily Workloads'

    def __str__(self):
        return self.daily_workload_date


class ClinicianExistingEMCAssessment(models.Model):
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)


class ClinicianNewEMCAssessment(models.Model):
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    total_time = models.TimeField(auto_now=False, auto_now_add=False)
    mode_of_assessment = models.TextField(null=True, blank=True)


class ClinicianClientReAssessment(models.Model):
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    total_time = models.TimeField(auto_now=False, auto_now_add=False)
    mode_of_assessment = models.TextField(null=True, blank=True)


class ClinicianClientStatusChoices(models.TextChoices):
    NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS = 'NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS', _(
        'Existing Extra-Mural Client - No Reassessment')
    NEW_CASE_CLIENT_EXISTING_EMC_REASSESS = 'NEW_CASE_CLIENT_EXISTING_EMC_REASSESS', _(
        'Existing Extra-Mural Client Reassessment')
    NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT = 'NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT', _(
        'New Extra-Mural Client Assessment')
    EXISTING_CASE_CLIENT_REASSESS = 'EXISTING_CASE_CLIENT_REASSESS', _('Existing Case Management Client Reassessment')


class ClinicianClientAssessment(models.Model):
    client_assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    clinician = models.ForeignKey(
        ClinicanUsers,
        on_delete=models.PROTECT,
        verbose_name="Clinician",
        db_column="clinician"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Clinician Assessment Client",
        db_column="clinician_client"
    )
    client_status = models.CharField(
        max_length=100,
        choices=ClinicianClientStatusChoices.choices,
        default=ClinicianClientStatusChoices.NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS,
        blank=True
    )
    existing_assessment = models.ForeignKey(
        ClinicianExistingEMCAssessment,
        on_delete=models.PROTECT,
        verbose_name="Existing Extra Mural Client Assessment",
        db_column="existing_emp_assessment",
        null=True,
        blank=True
    )
    reassessment = models.ForeignKey(
        ClinicianClientReAssessment,
        on_delete=models.PROTECT,
        verbose_name="Client Reassessment",
        db_column="client_reassessment",
        null=True,
        blank=True
    )
    newextramuralclient_assessment = models.ForeignKey(
        ClinicianNewEMCAssessment,
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


class Interventions(models.Model):
    intervention_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Clinician Intervention Client",
        db_column="client"
    )
    clinician = models.ForeignKey(
        ClinicanUsers,
        on_delete=models.PROTECT,
        verbose_name="Clinician",
        db_column="clinician"
    )
    date = models.DateField(null=True, blank=True)
    total_time = models.TimeField(auto_now=False, auto_now_add=False)
    mode_of_clinical_intervention = models.TextField(null=True, blank=True)
    clinical_type = models.TextField(null=True, blank=True)
    clinical_type_detail = models.TextField(null=True, blank=True)
    therapeutic_type = models.TextField(null=True, blank=True)
    therapeutic_type_detail = models.TextField(null=True, blank=True)
