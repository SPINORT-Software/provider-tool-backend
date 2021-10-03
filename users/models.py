from django.db import models
import uuid


class Users(models.Model):
    """
    User Entity.
    Primary record of a user in the application (irrespective of the type of user)
    """
    user_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=45, unique=True)
    password = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name} [{self.email}]"
