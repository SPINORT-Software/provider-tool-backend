from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from core.models import *
from rest_framework.serializers import ModelSerializer
from reviewboard.serializers import ReviewBoardUserSerializer


# class UserSerializer(serializers.ModelSerializer):
    # user_type = serializers.SerializerMethodField()

    # user_type_id = serializers.SerializerMethodField()
    #
    # def get_user_type(self, obj):
    #     user_type_object = UserType.objects.get(user=obj)
    #     user_type_text = UserTypeSerializer(user_type_object).data['type']
    #     return {
    #         "code": user_type_text,
    #         "object": self.get_user_type_object(user_type_text, obj)
    #     }
    #
    # def get_user_type_object(self, user_type, user_object):
    #     user_type_pk = {
    #         Types.TYPE_CLINICIAN: 'clinicianuser',
    #         Types.TYPE_REVIEW_BOARD: 'reviewboarduser'
    #     }
    #     user_type_serializers = {
    #         Types.TYPE_CLINICIAN: ClinicianUserSerializer,
    #         Types.TYPE_REVIEW_BOARD: ReviewBoardUserSerializer
    #     }
    #     user_type_pk = user_type_pk.get(user_type)
    #     user_type_object = getattr(user_object, user_type_pk)
    #     return user_type_serializers.get(user_type)(user_type_object).data

    # class Meta:
    #     model = User
    #     # fields = ('username', 'first_name', 'last_name', 'date_joined', 'user_type', 'id', 'user_type_id')
    #     # fields = ('username', 'first_name', 'last_name', 'date_joined', 'user_type', 'id')
    #     fields = ('username', 'first_name', 'last_name', 'date_joined', 'id')


# class UserSerializerWithToken(serializers.ModelSerializer):
    # token = serializers.SerializerMethodField()
    # password = serializers.CharField(write_only=True)
    #
    # def get_token(self, obj):
    #     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    #     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    #
    #     payload = jwt_payload_handler(obj)
    #     token = jwt_encode_handler(payload)
    #     return token
    #
    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance
    #
    # class Meta:
    #     model = User
    #     fields = ('token', 'username', 'password')

    # def filter_user(self, user_type, user):
    #     user_type_models = {
    #         Types.TYPE_CLINICIAN: {
    #             'model': ClinicanUsers,
    #             'pk': 'clinician_id'
    #         },
    #         Types.TYPE_REVIEW_BOARD: {
    #             'model': ReviewBoardUser,
    #             'pk': 'reviewboard_user_id'
    #         }
    #     }
    #     TypeData = user_type_models.get(user_type, None)
    #
    #     if TypeData:
    #         TypeModel = TypeData['model']
    #         TypeModel_pk = TypeData['pk']
    #         user_type_model_object = TypeModel.objects.get(user=user)
    #         return getattr(user_type_model_object, TypeModel_pk)
    #     return -1
