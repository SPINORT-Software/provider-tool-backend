from django.db import models
from users.models import Users
import uuid
from clientpatient.models import Client
from django.utils.translation import gettext_lazy as _


class ReviewBoardMember(models.Model):
    reviewboard_member_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        verbose_name="User - Review Board",
        db_column="user_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Review Board User"
        verbose_name_plural = "Review Board Users"

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}]"


class ReferralDecisionChoices(models.TextChoices):
    REFERRAL_ACCEPTED = 'REFERRAL_ACCEPTED', _('Client Accepted')
    REFERRAL_REFUSED = 'REFERRAL_REFUSED', _('Client Refused')


class ClientReferral(models.Model):
    referral_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    referral_date = models.DateTimeField(null=True, blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Referral Client",
        db_column="client"
    )
    referral_source = models.TextField()
    referral_source_detail = models.TextField()
    organizations_upon_referral = models.TextField()
    organizations_upon_referral_detail = models.TextField()
    date_of_case_discussion = models.DateTimeField(null=True, blank=True)
    members_present_case_discussion = models.TextField()
    members_present_case_discussion_detail = models.TextField()
    case_management_organization_responsible = models.TextField()
    case_management_user_responsible = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        verbose_name="Person Responsible for Client Case Management",
        db_column="case_management_user_responsible"
    )
    decision = models.CharField(
        max_length=20,
        choices=ReferralDecisionChoices.choices,
        default=ReferralDecisionChoices.REFERRAL_REFUSED,
    )
    decision_detail = models.TextField()
