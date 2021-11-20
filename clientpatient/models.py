from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings


class ClientStatus(models.TextChoices):
    ACTIVE_CLIENT = 'ACTIVE_CLIENT', _('Active Client')
    DISCHARGED_CLIENT = 'DISCHARGED_CLIENT', _('Discharged Client')
    POTENTIAL_CLIENT = 'POTENTIAL_CLIENT', _('Potential Client')


class Client(models.Model):
    """
    Client Entity.
    Primary record of a client in the application
    """
    client_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    client_active = models.BooleanField(default=False, verbose_name="Client Active")
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User - Client",
        db_column="user_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    client_status = models.CharField(
        max_length=100,
        choices=ClientStatus.choices,
        default=ClientStatus.POTENTIAL_CLIENT,
        blank=True
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name} [{self.client_id}]"


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.client.save()


class CommunicationLog(models.Model):
    log_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    person_completing = models.TextField(null=True, blank=True)
    person_completing_detail = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Client",
        db_column="client"
    )


class VisitorLog(models.Model):
    log_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    organization = models.TextField(null=True, blank=True)
    visit_reason = models.TextField(null=True, blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Client",
        db_column="client",
        blank=True,
        null=True
    )


class MedicalDiagnosis(models.Model):
    medical_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    cancer = models.TextField(null=True, blank=True)
    cardiac = models.TextField(null=True, blank=True)
    cardiac_detail = models.TextField(null=True, blank=True)
    circulatory = models.TextField(null=True, blank=True)
    circulatory_detail = models.TextField(null=True, blank=True)
    integumentary = models.TextField(null=True, blank=True)
    integumentary_detail = models.TextField(null=True, blank=True)
    endocrine = models.TextField(null=True, blank=True)
    endocrine_detail = models.TextField(null=True, blank=True)
    eye = models.TextField(null=True, blank=True)
    eye_detail = models.TextField(null=True, blank=True)
    frailty = models.TextField(null=True, blank=True)
    gastro_intestinal = models.TextField(null=True, blank=True)
    musculoskeletal = models.TextField(null=True, blank=True)
    musculoskeletal_detail = models.TextField(null=True, blank=True)
    neurological = models.TextField(null=True, blank=True)
    neurological_detail = models.TextField(null=True, blank=True)
    obesity = models.TextField(null=True, blank=True)
    post_surgical = models.TextField(null=True, blank=True)
    genital_urinary = models.TextField(null=True, blank=True)
    genital_urinary_detail = models.TextField(null=True, blank=True)
    respiratory = models.TextField(null=True, blank=True)
    respiratory_detail = models.TextField(null=True, blank=True)
    substance_abuse = models.TextField(null=True, blank=True)


class HomeSupportServices(models.Model):
    home_support_services_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    informal_support = models.TextField(null=True, blank=True)
    informal_support_detail = models.TextField(null=True, blank=True)
    formal_support = models.TextField(null=True, blank=True)
    formal_support_detail = models.TextField(null=True, blank=True)


class PreviousHospitalization(models.Model):
    previous_hospitalization_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    hospitalizations_six_months = models.IntegerField(null=True, blank=True, default=0)
    hospitalizations_twelve_months = models.IntegerField(null=True, blank=True, default=0)
    hospitalization_last_date = models.DateField(null=True, blank=True)
    hospitalization_last_stay_length = models.IntegerField(null=True, blank=True)
    hospitalization_last_medical_reason = models.TextField(null=True, blank=True)


class EmergencyRoomVisits(models.Model):
    emergency_room_visit_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    emergency_room_count_six_months = models.IntegerField(null=True, blank=True)
    emergency_room_count_twelve_months = models.IntegerField(null=True, blank=True)
    emergency_room_last_date = models.DateField(null=True, blank=True)
    emergency_room_last_medical_reason = models.TextField(null=True, blank=True)


class AmbulanceUse(models.Model):
    ambulance_use_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    ambulance_use_six_months = models.IntegerField(null=True, blank=True)
    ambulance_use_medical_reason_six_months = models.TextField(null=True, blank=True)
    ambulance_use_twelve_months = models.IntegerField(null=True, blank=True)
    ambulance_use_medical_reason_twelve_months = models.TextField(null=True, blank=True)


class ClinicalInformation(models.Model):
    clinical_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    client = models.OneToOneField(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Client",
        db_column="client"
    )
    completion_date = models.DateField(auto_now_add=True)
    revision_date = models.DateField(null=True, blank=True)
    medical_diagnosis = models.ForeignKey(
        MedicalDiagnosis,
        on_delete=models.PROTECT,
        verbose_name="Medical Diagnosis",
        db_column="medical_diagnosis",
        blank=True,
        null=True
    )
    home_support_services = models.ForeignKey(
        HomeSupportServices,
        on_delete=models.PROTECT,
        verbose_name="Home Support Services",
        db_column="home_support_services",
        blank=True,
        null=True
    )
    last_hospitalization = models.ForeignKey(
        PreviousHospitalization,
        on_delete=models.PROTECT,
        verbose_name="Last Hospitalization",
        db_column="last_hospitalization",
        blank=True,
        null=True
    )
    emergency_room_visits = models.ForeignKey(
        EmergencyRoomVisits,
        on_delete=models.PROTECT,
        verbose_name="ER Visits",
        db_column="emergency_room_visits",
        blank=True,
        null=True
    )
    ambulance_use = models.ForeignKey(
        AmbulanceUse,
        on_delete=models.PROTECT,
        verbose_name="Ambulance Use",
        db_column="ambulance_use",
        blank=True,
        null=True
    )
    family_physician = models.TextField(null=True, blank=True)
    nurse_practitioner = models.TextField(null=True, blank=True)
    past_medical_history = models.TextField(null=True, blank=True)


class CurrentMedication(models.Model):
    medication_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    medication_name = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    dosage = models.TextField(null=True, blank=True)
    intake_frequency = models.TextField(null=True, blank=True)
    clinical_id = models.ForeignKey(
        ClinicalInformation,
        on_delete=models.PROTECT,
        verbose_name="Clinical Information",
        db_column="clinical_id"
    )


class PersonalInformation(models.Model):
    personal_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    completion_date = models.DateField(auto_now_add=True)
    revision_date = models.DateField(null=True, blank=True)
    client = models.OneToOneField(
        Client,
        unique=True,
        on_delete=models.PROTECT,
        verbose_name="Client",
        db_column="client"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.TextField(null=True, blank=True)
    ethnic_background = models.TextField(null=True, blank=True)
    ethnic_background_detail = models.TextField(null=True, blank=True)
    language_proficiency_english = models.TextField(null=True, blank=True)
    language_proficiency_french = models.TextField(null=True, blank=True)
    language_proficiency_other = models.TextField(null=True, blank=True)
    language_proficiency_interpreter = models.TextField(null=True, blank=True)
    marital_status = models.TextField(null=True, blank=True)
    marital_status_detail = models.TextField(null=True, blank=True)
    family_situation = models.TextField(null=True, blank=True)
    family_situation_detail = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    education_detail = models.TextField(null=True, blank=True)
    employment = models.TextField(null=True, blank=True)
    employment_detail = models.TextField(null=True, blank=True)
    household_income = models.TextField(null=True, blank=True)
    household_income_detail = models.TextField(null=True, blank=True)
    housing_situation = models.TextField(null=True, blank=True)
    housing_situation_detail = models.TextField(null=True, blank=True)


class HomeSafetyAssessment(models.Model):
    answer_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    personal_information = models.ForeignKey(
        PersonalInformation,
        on_delete=models.PROTECT,
        verbose_name="Personal Information",
        db_column="personal_information",
        default=None
    )
    question_group = models.TextField(null=True, blank=True)
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    answer_detail = models.TextField(null=True, blank=True)
