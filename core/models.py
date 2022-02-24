from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Types(models.TextChoices):
    TYPE_CLIENT = 'TYPE_CLIENT', _('CLIENT')
    TYPE_CLINICIAN = 'TYPE_CLINICIAN', _('CLINICIAN')
    TYPE_REVIEW_BOARD = 'TYPE_REVIEW_BOARD', _('REVIEW BOARD')
    TYPE_COMMUNITY_PARAMEDIC = 'TYPE_COMMUNITY_PARAMEDIC', _('COMMUNITY PARAMEDIC')
    TYPE_CASE_MANAGER = 'TYPE_CASE_MANAGER', _('CASE MANAGER')
    TYPE_ADMIN = 'TYPE_ADMIN', _('ADMIN')
    TYPE_NORMAL_USER = 'TYPE_NORMAL_USER', _('NORMAL USER')


class ProviderTypes(models.TextChoices):
    PROVIDER_TYPE_ADMINISTRATION = 'PROVIDER_TYPE_ADMINISTRATION', _('DEFAULT')
    PROVIDER_TYPE_DEFAULT = 'PROVIDER_TYPE_DEFAULT', _('DEFAULT')
    PROVIDER_TYPE_NUTRITIONIST = 'PROVIDER_TYPE_NUTRITIONIST', _('NUTRITIONIST')
    PROVIDER_TYPE_OCCUPATIONAL_THERAPIST = 'PROVIDER_TYPE_OCCUPATIONAL_THERAPIST', _('OCCUPATIONAL THERAPIST')
    PROVIDER_TYPE_PHYSICAL_THERAPIST = 'PROVIDER_TYPE_PHYSICAL_THERAPIST', _('PHYSICAL THERAPIST')
    PROVIDER_TYPE_REGISTERED_NURSE = 'PROVIDER_TYPE_REGISTERED_NURSE', _('REGISTERED NURSE')
    PROVIDER_TYPE_LICENSED_PRACTICAL_NURSE = 'PROVIDER_TYPE_LICENSED_PRACTICAL_NURSE', _('LICENSED PRACTICAL NURSE')
    PROVIDER_TYPE_RESPIRATORY_THERAPIST = 'PROVIDER_TYPE_RESPIRATORY_THERAPIST', _('RESPIRATORY THERAPIST')
    PROVIDER_TYPE_SOCIAL_WORKER = 'PROVIDER_TYPE_SOCIAL_WORKER', _('SOCIAL WORKER')
    PROVIDER_TYPE_SPEECH_LANGUAGE_THERAPIST = 'PROVIDER_TYPE_SPEECH_LANGUAGE_THERAPIST', _('SPEECH LANGUAGE THERAPIST')


class OrganizationChoices(models.TextChoices):
    ORGANIZATION_ABILITY_NB = 'ORGANIZATION_ABILITY_NB', _('Ability NB')
    ORGANIZATION_AMBULATORY_CLINIC = 'ORGANIZATION_AMBULATORY_CLINIC', _('Ambulatory Clinic (Outpatient)')
    ORGANIZATION_AMBULANCE_NEW_BRUNSWICK = 'ORGANIZATION_AMBULANCE_NEW_BRUNSWICK', _('Ambulance New Brunswick (ANB)')
    ORGANIZATION_COMMUNITY_HEALTH_CENTERS = 'ORGANIZATION_COMMUNITY_HEALTH_CENTERS', _('Community Health Centers')
    ORGANIZATION_DEPARTMENT_OF_VETERAN_AFFAIRS = 'ORGANIZATION_DEPARTMENT_OF_VETERAN_AFFAIRS', _(
        'Department of Veteran Affairs')
    ORGANIZATION_EMERGENCY_DEPARTMENT = 'ORGANIZATION_EMERGENCY_DEPARTMENT', _('Emergency Department')
    ORGANIZATION_EXTRA_MURAL_PROGRAM = 'ORGANIZATION_EXTRA_MURAL_PROGRAM', _('Extra-Mural Program')
    ORGANIZATION_FAMILY_PHYSICIAN_OUTSIDE_COMMUNITY_HEALTH_CENTERS = 'ORGANIZATION_FAMILY_PHYSICIAN_OUTSIDE_COMMUNITY_HEALTH_CENTERS', _(
        'Family Physician (Outside Community Health Centers)')
    ORGANIZATION_FIRST_NATIONS = 'ORGANIZATION_FIRST_NATIONS', _('First Nations')
    ORGANIZATION_HOMECARE_AGENCY = 'ORGANIZATION_HOMECARE_AGENCY', _('Homecare Agency')
    ORGANIZATION_HOSPITAL_INPATIENT = 'ORGANIZATION_HOSPITAL_INPATIENT', _('Hospital (Inpatient)')
    ORGANIZATION_NURSING_HOME = 'ORGANIZATION_NURSING_HOME', _('Nursing Home')
    ORGANIZATION_PUBLIC_HEALTH_SERVICES = 'ORGANIZATION_PUBLIC_HEALTH_SERVICES', _('Public Health Services')
    ORGANIZATION_RESIDENTIAL_FACILITY = 'ORGANIZATION_RESIDENTIAL_FACILITY', _('Residential Facility')
    ORGANIZATION_SOCIAL_DEVELOPMENT = 'ORGANIZATION_SOCIAL_DEVELOPMENT', _('Social Development')
    ORGANIZATION_OTHER = 'ORGANIZATION_OTHER', _('Other')


class Organizations(models.Model):
    organization_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    organization_name = models.TextField(null=True, blank=True)


# class UserType(models.Model):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.PROTECT,
#         verbose_name="User",
#         unique=True
#     )
#     type = models.CharField(
#         max_length=100,
#         choices=Types.choices,
#         default=Types.TYPE_NORMAL_USER
#     )
#
#     def __str__(self):
#         return self.user.first_name + " " + self.user.last_name
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.usertype.save()


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


class ExternalPartnerClientStatusChoices(models.TextChoices):
    NEW_CASE_MANAGEMENT_CLIENT = 'NEW_CASE_MANAGEMENT_CLIENT', _(
        'New Case Management Client')
    EXISTING_CASE_MANAGEMENT_CLIENT = 'EXISTING_CASE_MANAGEMENT_CLIENT', _('Existing Case Management Client')
