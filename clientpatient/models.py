from django.db import models
import uuid
from users.models import Users


class Client(models.Model):
    """
    Client Entity.
    Primary record of a client in the application
    """
    client_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    client_active = models.BooleanField(default=False, verbose_name="Client Active")
    user_id = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        verbose_name="User - Client",
        db_column="user_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"
