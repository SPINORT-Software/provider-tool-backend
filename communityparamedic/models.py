from django.db import models
from users.models import Users
from clientpatient.models import Client
import uuid
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from authentication.models import Types as UserTypes, ApplicationUser
from core.models import ProviderTypes

class DailyWorkLoad(models.Model):
    daily_workload_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    community_paramedic = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Community Paramedic",
        db_column="community_paramedic",
        null=True,
        blank=True,
        related_name="paramedic_dailyworkload"
    )
    daily_workload_date = models.DateField(null=True, blank=True)
    client_caseload_casemanagement_number_clients = models.IntegerField(null=True)
    client_caseload_casemanagement_total_time = models.TimeField(auto_now=False, auto_now_add=False)
    client_caseload_regular_number_clients = models.IntegerField(null=True)
    client_caseload_regular_total_time = models.TimeField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "Daily Workload"
        verbose_name_plural = "Daily Workloads"

    def __str__(self):
        return f"{self.daily_workload_date}"


class ClientStatusChoices(models.TextChoices):
    EXISTING_CASE_MANAGEMENT_CLIENT = 'EXISTING_CASE_MANAGEMENT_CLIENT', _('Existing Case Management Client')
    NEW_CASE_MANAGEMENT_CLIENT = 'NEW_CASE_MANAGEMENT_CLIENT', _('New Case Management Client')


class ClientVitalSigns(models.Model):
    vital_signs_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    bp_value = models.TextField(null=True, blank=True)
    pulse_value = models.TextField(null=True, blank=True)
    hr_value = models.TextField(null=True, blank=True)
    rr_value = models.TextField(null=True, blank=True)
    temp_value = models.TextField(null=True, blank=True)
    weight_value = models.TextField(null=True, blank=True)
    oximetry_choice = models.TextField(null=True, blank=True)
    oximetry_value = models.TextField(null=True, blank=True)
    last_weight = models.TextField(null=True, blank=True)
    last_weight_date = models.DateField(null=True, blank=True)


class NewCaseClientAssessment(models.Model):
    """
    Type of Client Assessment (this is not the primary record for Client Assessment)
    """
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    vital_signs = models.ForeignKey(
        ClientVitalSigns,
        on_delete=models.PROTECT,
        verbose_name="Vital Signs",
        db_column="vital_signs"
    )
    priority_problems = models.TextField(null=True, blank=True)
    priority_problems_detail = models.TextField(null=True, blank=True)
    interventions = models.TextField(null=True, blank=True)
    interventions_detail = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)
    recommendations_detail = models.TextField(null=True, blank=True)
    risks_changes_reported_to_emp = models.BooleanField(default=False)
    reported_provider_name = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        verbose_name="Provider",
        db_column="reported_provider"
    )


class ExistingCaseClientAssessmentChangeInCondition(models.Model):
    change_in_condition_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    mental_status_changes = models.TextField()
    functional_status_changes = models.TextField()
    respiratory_changes = models.TextField()
    gi_abdomen_changes = models.TextField()
    gi_abdomen_changes_detail = models.TextField(blank=True, null=True)
    gu_urine_changes = models.TextField()


class ExistingCaseClientAssessment(models.Model):
    """
    Type of Client Assessment (this is not the primary record for Client Assessment)
    """
    assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)

    assessment_change_in_condition = models.BooleanField(default=False)
    assessment_change_in_condition_detail = models.TextField(null=True, blank=True)
    assessment_changes_perceived_date = models.DateField(null=True, blank=True)
    assessment_condition_worse_reasons = models.TextField(null=True, blank=True)
    assessment_condition_better_reasons = models.TextField(null=True, blank=True)
    assessment_condition_occurred_before = models.BooleanField(default=False)
    assessment_treatment_last_episode = models.TextField(null=True, blank=True)
    assessment_other_information = models.TextField(null=True, blank=True)

    changes_in_condition = models.ForeignKey(
        ExistingCaseClientAssessmentChangeInCondition,
        on_delete=models.PROTECT,
        verbose_name="Changes in Condition",
        db_column="condition_changes"
    )
    vital_signs = models.ForeignKey(
        ClientVitalSigns,
        on_delete=models.PROTECT,
        verbose_name="Vital Signs",
        db_column="vital_signs"
    )
    priority_problems = models.TextField(null=True, blank=True)
    priority_problems_detail = models.TextField(null=True, blank=True)

    interventions = models.TextField(null=True, blank=True)
    interventions_detail = models.TextField(null=True, blank=True)

    recommendations = models.TextField(null=True, blank=True)
    recommendations_detail = models.TextField(null=True, blank=True)

    risks_changes_reported_to_emp = models.BooleanField(default=False)
    reported_provider_name = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        verbose_name="Provider",
        db_column="reported_provider"
    )


class CommunityClientAssessment(models.Model):
    """
    Primary Client Assessment Class - this is the primary record created for a Community Paramedic's Client
    Assessment.
    """
    client_assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    community_paramedic = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Community Paramedic",
        db_column="community_paramedic",
        related_name="paramedic_clientassessment"
    )
    client = models.ForeignKey(
        ApplicationUser,
        on_delete=models.PROTECT,
        verbose_name="Assessment Client",
        db_column="client",
        related_name="paramedic_clientassessment_client"
    )
    client_status = models.CharField(
        max_length=100,
        choices=ClientStatusChoices.choices,
        default=ClientStatusChoices.NEW_CASE_MANAGEMENT_CLIENT,
        blank=True
    )
    new_case_client_assessment = models.ForeignKey(
        NewCaseClientAssessment,
        on_delete=models.PROTECT,
        verbose_name="New Case Management Client Assessment",
        db_column="new_case_client_assessment",
        null=True,
        blank=True
    )
    existing_case_client_assessment = models.ForeignKey(
        ExistingCaseClientAssessment,
        on_delete=models.PROTECT,
        verbose_name="Existing Case Client Assessment",
        db_column="existing_case_client_assessment",
        null=True,
        blank=True
    )


class HomeSafetyAssessment(models.Model):
    answer_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    new_client_assessment = models.ForeignKey(
        NewCaseClientAssessment,
        on_delete=models.PROTECT,
        verbose_name="New Case Client Assessment",
        db_column="new_client_assessment",
        default=None
    )
    question = models.TextField()
    answer = models.IntegerField(default=False)
    answer_detail = models.TextField(null=True, blank=True)




# class CommunityParamedicUser(models.Model):
#     community_paramedic_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         related_name='communityparamedicuser',
#         on_delete=models.PROTECT,
#         verbose_name="User - Community Paramedic",
#         db_column="user_id"
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
#         verbose_name = "Community Paramedic"
#         verbose_name_plural = "Community Paramedics"
#
#     def __str__(self):
#         return f"{self.user_id.first_name} {self.user_id.last_name}"


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_communityparamedicuser(sender, instance, created, **kwargs):
#     if created:
#         if hasattr(instance, 'user_type') and instance.user_type == UserTypes.TYPE_COMMUNITY_PARAMEDIC:
#             CommunityParamedicUser.objects.create(user=instance)
#
