import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None, user_type=None, first_name=None, last_name=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.user_type = user_type
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Types(models.TextChoices):
    TYPE_CLIENT = 'TYPE_CLIENT', _('CLIENT')
    TYPE_CLINICIAN = 'TYPE_CLINICIAN', _('CLINICIAN')
    TYPE_REVIEW_BOARD = 'TYPE_REVIEW_BOARD', _('REVIEW BOARD')
    TYPE_COMMUNITY_PARAMEDIC = 'TYPE_COMMUNITY_PARAMEDIC', _('COMMUNITY PARAMEDIC')
    TYPE_CASE_MANAGER = 'TYPE_CASE_MANAGER', _('CASE MANAGER')
    TYPE_ADMIN = 'TYPE_ADMIN', _('ADMIN')
    TYPE_NORMAL_USER = 'TYPE_NORMAL_USER', _('NORMAL USER')


class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    first_name = models.TextField()

    last_name = models.TextField()

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    is_staff = models.BooleanField(default=False)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    user_type = models.CharField(
        max_length=100,
        choices=Types.choices,
        default=Types.TYPE_NORMAL_USER
    )

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    # user_type_pk = {
    #     'TYPE_REVIEW_BOARD': (ReviewBoardUser, 'reviewboard_user_id')
    # }

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    @property
    def user_type_pk(self):
        """
        Get user type model instance.
        """
        return self._get_user_type_instance()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'username': self.username,
            'email': self.email,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def _get_user_type_instance(self):
        """
        Get the user type model PK value for frontend.
        :return:
        """
        try:
            user_type_models = {
                'TYPE_REVIEW_BOARD': ('reviewboarduser', 'reviewboard_user_id'),
                'TYPE_CLINICIAN': ('clinicianuser', 'clinician_id'),
                'TYPE_CLIENT': ('clientuser', 'client_id'),
                'TYPE_COMMUNITY_PARAMEDIC': ('communityparamedicuser', 'community_paramedic_id'),
            }
            user_type_data = user_type_models.get(self.user_type, None)
            if user_type_data:
                user_type_model_field = user_type_data[0]
                user_type_model_pk = user_type_data[1]
                user_type_instance = getattr(self, user_type_model_field)
                return getattr(user_type_instance, user_type_model_pk)
            return False
        except Exception as e:
            return False
