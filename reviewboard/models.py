from django.db import models
from users.models import Users
import uuid
from clientpatient.models import Client, ClientStatus
from django.utils.translation import gettext_lazy as _


class ReviewBoardUser(models.Model):
    reviewboard_user_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        verbose_name="User",
        db_column="user_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Review Board User"
        verbose_name_plural = "Review Board Users"

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"


class ClientReferral(models.Model):
    referral_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    referral_date = models.DateField(null=True, blank=True)
    review_board_user = models.ForeignKey(
        ReviewBoardUser,
        on_delete=models.PROTECT,
        verbose_name="Review Board User",
        db_column="review_board_user"
    )
    client_first_name = models.TextField()
    client_last_name = models.TextField()
    client_email = models.TextField()
    referral_source = models.TextField(null=True, blank=True)
    referral_source_detail = models.TextField(null=True, blank=True)
    organizations_upon_referral = models.TextField(null=True, blank=True)
    organizations_upon_referral_detail = models.TextField(null=True, blank=True)
    date_of_case_discussion = models.DateField(null=True, blank=True)
    members_present_case_discussion = models.TextField(null=True, blank=True)
    members_present_case_discussion_detail = models.TextField(null=True, blank=True)
    case_management_organization_responsible = models.TextField(null=True, blank=True)
    case_management_organization_person_responsible = models.TextField(null=True, blank=True)
    decision = models.CharField(
        max_length=20,
        choices=ClientStatus.choices,
        default=ClientStatus.POTENTIAL_CLIENT,
    )
    decision_detail = models.TextField()
