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
    PROVIDER_TYPE_DEFAULT = 'PROVIDER_TYPE_DEFAULT', _('DEFAULT')
    PROVIDER_TYPE_NUTRITIONIST = 'PROVIDER_TYPE_NUTRITIONIST', _('NUTRITIONIST')
    PROVIDER_TYPE_OCCUPATIONAL_THERAPIST = 'PROVIDER_TYPE_OCCUPATIONAL_THERAPIST', _('OCCUPATIONAL THERAPIST')
    PROVIDER_TYPE_PHYSICAL_THERAPIST = 'PROVIDER_TYPE_PHYSICAL_THERAPIST', _('PHYSICAL THERAPIST')
    PROVIDER_TYPE_REGISTERED_NURSE = 'PROVIDER_TYPE_REGISTERED_NURSE', _('REGISTERED NURSE')
    PROVIDER_TYPE_RESPIRATORY_THERAPIST = 'PROVIDER_TYPE_RESPIRATORY_THERAPIST', _('RESPIRATORY THERAPIST')
    PROVIDER_TYPE_SOCIAL_WORKER = 'PROVIDER_TYPE_SOCIAL_WORKER', _('SOCIAL WORKER')
    PROVIDER_TYPE_SPEECH_LANGUAGE_THERAPIST = 'PROVIDER_TYPE_SPEECH_LANGUAGE_THERAPIST', _('SPEECH LANGUAGE THERAPIST')


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
