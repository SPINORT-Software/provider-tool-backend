from django.db import models
from users.models import Users
from clientpatient.models import Client
import uuid
from django.utils.translation import gettext_lazy as _


class CommunityParamedic(models.Model):
    community_paramedic_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        verbose_name="User - Community Paramedic",
        db_column="user_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Community Paramedic"
        verbose_name_plural = "Community Paramedics"

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}]"


class DailyWorkLoad(models.Model):
    daily_workload_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    community_paramedic = models.ForeignKey(
        CommunityParamedic,
        on_delete=models.PROTECT,
        verbose_name="Community Paramedic",
        db_column="community_paramedic"
    )

    daily_workload_date = models.DateTimeField(null=True, blank=True)

    client_caseload_casemanagement_number_clients = models.IntegerField(null=True)
    client_caseload_casemanagement_total_time = models.TimeField(auto_now=False, auto_now_add=False)

    client_caseload_regular_number_clients = models.IntegerField(null=True)
    client_caseload_regular_total_time = models.TimeField(auto_now=False, auto_now_add=False)


class ClientStatusChoices(models.TextChoices):
    EXISTING_CASE_MANAGEMENT_CLIENT = 'EXISTING_CASE_MANAGEMENT_CLIENT', _('Existing Case Management Client')
    NEW_CASE_MANAGEMENT_CLIENT = 'NEW_CASE_MANAGEMENT_CLIENT', _('New Case Management Client')


class ClientAssessmentMaster(models.Model):
    client_assessment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    community_paramedic = models.ForeignKey(
        CommunityParamedic,
        on_delete=models.PROTECT,
        verbose_name="Community Paramedic",
        db_column="community_paramedic"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Assessment Client",
        db_column="client"
    )


class HomeSafetyAssessmentQuestionGroup(models.Model):
    question_group_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    question_group_label = models.TextField()
    question_group_code = models.TextField()


class HomeSafetyAssessmentQuestions(models.Model):
    question_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    question_group = models.ForeignKey(
        HomeSafetyAssessmentQuestionGroup,
        on_delete=models.PROTECT,
        verbose_name="Question Group",
        db_column="question_group"
    )
    question = models.TextField()


class NewClientAssessment(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    departure_time = models.TimeField(auto_now=False, auto_now_add=False)
    assessment_master = models.ForeignKey(
        ClientAssessmentMaster,
        on_delete=models.PROTECT,
        verbose_name="Client Assessment",
        db_column="assessment_master"
    )


class HomeSafetyAssessmentQuestionAnswers(models.Model):
    answer_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    new_client_assessment = models.ForeignKey(
        NewClientAssessment,
        on_delete=models.PROTECT,
        verbose_name="New Client Assessment Record",
        db_column="new_client_assessment"
    )
    question = models.ForeignKey(
        HomeSafetyAssessmentQuestions,
        on_delete=models.PROTECT,
        verbose_name="Question",
        db_column="question"
    )
    answer = models.BooleanField()
    answer_detail = models.TextField(null=True, blank=True)
