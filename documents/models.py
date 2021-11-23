from django.db import models
import uuid
from casemanager.models import CaseManagerClientAssessment, ClientIntervention
from clinician.models import ClinicianClientAssessment
from reviewboard.models import ClientReferral
from communityparamedic.models import NewCaseClientAssessment, ExistingCaseClientAssessment
from django.conf import settings


class DocumentTypes(models.Model):
    type_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    type_label = models.TextField()
    type_code = models.TextField()

    class Meta:
        verbose_name = "Document Type"
        verbose_name_plural = "Document Types"

    def __str__(self):
        return self.type_label


class Documents(models.Model):
    document_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    path = models.TextField(blank=True)
    type = models.ForeignKey(
        DocumentTypes,
        on_delete=models.PROTECT,
        verbose_name="Document Type",
        db_column="type"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User",
        db_column="user_id",
        default=None
    )

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.name


class CaseManagerAssessmentFormsDocuments(models.Model):
    assessment_form_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Documents,
        on_delete=models.PROTECT,
        verbose_name="Document",
        db_column="document"
    )
    client_assessment = models.ForeignKey(
        CaseManagerClientAssessment,
        on_delete=models.PROTECT,
        verbose_name="Client Assessment",
        db_column="client_assessment"
    )
    assessment_type = models.TextField()
    is_provider_form = models.BooleanField(default=False)


class ClinicianAssessmentFormsDocuments(models.Model):
    assessment_form_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Documents,
        on_delete=models.PROTECT,
        verbose_name="Document",
        db_column="document"
    )
    client_assessment = models.ForeignKey(
        ClinicianClientAssessment,
        on_delete=models.PROTECT,
        verbose_name="Client Assessment",
        db_column="client_assessment"
    )
    assessment_type = models.TextField()
    is_provider_form = models.BooleanField(default=False)


class InterventionFormsDocuments(models.Model):
    intervention_form_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Documents,
        on_delete=models.PROTECT,
        verbose_name="Document",
        db_column="document"
    )
    client_intervention = models.ForeignKey(
        ClientIntervention,
        on_delete=models.PROTECT,
        verbose_name="Client Intervention",
        db_column="client_intervention"
    )


class ReviewBoardReferralFormsDocuments(models.Model):
    referral_form_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Documents,
        on_delete=models.PROTECT,
        verbose_name="Document",
        db_column="document"
    )
    client_referral = models.ForeignKey(
        ClientReferral,
        on_delete=models.PROTECT,
        verbose_name="Client Referral",
        db_column="client_referral"
    )


class NewClientCommunityParamedicFormsDocuments(models.Model):
    form_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Documents,
        on_delete=models.PROTECT,
        verbose_name="Document",
        db_column="document"
    )
    client_assessment = models.ForeignKey(
        NewCaseClientAssessment,
        on_delete=models.PROTECT,
        verbose_name="New Client Assessment",
        db_column="client_assessment"
    )


class ExistingClientCommunityParamedicFormsDocuments(models.Model):
    form_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Documents,
        on_delete=models.PROTECT,
        verbose_name="Document",
        db_column="document"
    )
    client_assessment = models.ForeignKey(
        ExistingCaseClientAssessment,
        on_delete=models.PROTECT,
        verbose_name="Existing Client Assessment",
        db_column="client_assessment"
    )
