from django.db import models
import uuid
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class Attachment(models.Model):
    ATTACHMENT_TYPES = (
        ('CASE_MANAGER_DAILY_WORKLOAD', 'CM_DW'),
        ('CASE_MANAGER_CLIENT_ASSESSMENT', 'CM_CA'),
        ('CASE_MANAGER_CLIENT_INTERVENTION', 'CM_CI'),
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100, choices=ATTACHMENT_TYPES)
    attachment_uuid = models.CharField(max_length=56)


class MessageManager(models.Manager):
    def inbox_for(self, username):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        return self.filter(
            recipient__username=username
        )

    def outbox_for(self, username):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
            sender__username=username,
            sender_deleted_at__isnull=True,
        )

    def conversations_for(self, username):
        return self.filter(
            Q(sender__username=username) | Q(recipient__username=username)
        )

    def recipients_for(self, username):
        print(username)
        # return self.values('recipient').filter(Q(sender__username=username)).order_by('recipient').distinct('recipient')

        return self.values('recipient').filter(
            Q(sender__username=username) | Q(recipient__username=username)
        ).order_by('recipient').distinct('recipient')
    # | Q(recipient__username=username)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        verbose_name="Sender",
        on_delete=models.PROTECT
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        verbose_name="Recipient",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    body = models.TextField(_("Message"))
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)
    is_attachment = models.BooleanField(default=False, null=True, blank=True)
    attachment_id = models.ForeignKey(
        Attachment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = MessageManager()

    def save(self, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()

        super().save(**kwargs)

    class Meta:
        ordering = ['sent_at']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return self.body + " - " + self.sender.username + " to " + self.recipient.username
