from rest_framework import serializers

from .models import User, ApplicationUser, OrganizationChoices, Types, ProviderTypes
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['token', 'user_type', 'user_type_pk', 'provider_type', 'username', 'fullname']


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_type', 'user_type_pk', 'provider_type', 'username', 'first_name', 'last_name', 'fullname']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_type', 'user_type_pk', 'first_name', 'last_name', 'fullname']


class UserBasicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_type', 'first_name', 'last_name', 'fullname', 'email']


class ApplicationUserSearchRequestDataSerializer(serializers.Serializer):
    user__user_type = serializers.ChoiceField(choices=Types.choices, required=False, allow_blank=True)
    organization = serializers.ChoiceField(choices=OrganizationChoices.choices, required=False, allow_blank=True)
    provider_type = serializers.ChoiceField(choices=ProviderTypes.choices, required=False, allow_blank=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)


class ApplicationUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserBasicDetailSerializer(instance.user).data

        return response


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token', 'user_type', 'first_name', 'last_name']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    user_type = serializers.CharField(max_length=128, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    user_type_pk = serializers.CharField(max_length=255, read_only=True)
    provider_type = serializers.CharField(max_length=255, read_only=True)
    organization = serializers.CharField(max_length=255, read_only=True)
    fullname = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
            'user_type': user.user_type,
            'provider_type': user.provider_type,
            'organization': user.organization,
            'user_type_pk': user.user_type_pk,
            'fullname': user.fullname
        }
