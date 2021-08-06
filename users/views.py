from django.shortcuts import render
from entities.models import UserEntity, UserRoleEntityData, \
    UserRoleAttribute, UserRoleAttributeValues, UserRoleEntityDataTypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .model import accounts


class UserEntity(APIView):
    """
    List all users or create a user.
    """

    def post(self, request):
        """
        Add a new user record.
        :param request:
        :return:
        """
        pass

    def get(self, request):
        """
        Get all the user entity records.
        :param request:
        :return:
        """
        pass


class UserAccountValidate(APIView):
    pass


class UserEntityDetail(APIView):
    """
    API Class for User Detail
    """

    def put(self, request, user_id):
        """
        Update a User entity record.
        :param request:
        :return:
        """
        pass

    def delete(self, request, user_id):
        """
        Delete a user entity record.
        :param request:
        :return:
        """
        pass


class Role(APIView):
    """
    List all roles or create a role.
    """

    def post(self, request):
        """
        Add a new role record.
        :param request:
        :return:
        """
        pass

    def get(self, request):
        """
        Get all the role records.
        :param request:
        :return:
        """
        pass


class RoleDetail(APIView):
    """
    API Class for Role Detail
    """

    def put(self, request, role_id):
        """
        Update a role entity record.
        :param request:
        :return:
        """
        pass

    def delete(self, request, role_id):
        """
        Delete a role entity record.
        :param request:
        :return:
        """
        pass


class RolePermission(APIView):
    """
    List all role permissions or create a role permission.
    """

    def post(self, request):
        """
        Add a new role permission.
        :param request:
        :return:
        """
        pass

    def get(self, request):
        """
        Get all the role permissions.
        :param request:
        :return:
        """
        pass


class RolePermissionDetail(APIView):
    """
    API Class for Role Permission Detail
    """

    def put(self, request, role_permission_id):
        """
        Update a role permission entity record.
        :param role_permission_id:
        :param request:
        :return:
        """
        pass

    def delete(self, request, role_permission_id):
        """
        Delete a role permission entity record.
        :param role_permission_id:
        :param request:
        :return:
        """
        pass


class UserRole(APIView):
    """
    List all user role or create a user role.
    """

    def post(self, request):
        """
        Add a new user role record.
        :param request:
        :return:
        """
        pass

    def get(self, request):
        """
        Get all the user role records.
        :param request:
        :return:
        """
        pass


class UserRoleDetail(APIView):
    """
    API Class for User Role Detail
    """

    def put(self, request, user_role_id):
        """
        Update a user role entity record.
        :param user_role_id:
        :param request:
        :return:
        """
        pass

    def delete(self, request, user_role_id):
        """
        Delete a user role entity record.
        :param user_role_id:
        :param request:
        :return:
        """
        pass


class AccountEntity(APIView):
    """
    List all user entity types or create a user type
    To create a case manager, client, clinician, paramedic and a research team member
    """

    def __init__(self):
        self.accounts_model = accounts.Accounts()

    def post(self, request, role):
        """
        Add a new account record.
        - Create a user entity record and Get the user ID
        - For a case manager - Create a case manager entity record and get the case manager ID
        - Note: For other user type like Client - create respective entity record and get the entity ID
        - Create a role entity record and assign case manager ID to role ID of case manager
        :param request:
        :return:
        """
        try:
            response = self.accounts_model.create_account(request.data.get('user_data'), role)
            return response.get_response()
        except AttributeError:
            return Response({
                'result': False,
                'message': 'Missing required request fields.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Get all the user type entity records.
        - Get all records from user type entity table + user entity joined
        - List by pagination
        :param request:
        :return:
        """
        return Response(True)


class AccountEntityDetail(APIView):
    """
    API Class for User type entity record detail.
    """

    def put(self, request, casemgr_id):
        """
        Update a User type entity record.
        :param casemgr_id:
        :param request:
        :return:
        """
        pass

    def delete(self, request, casemgr_id):
        """
        Delete a User type entity record.
        :param casemgr_id:
        :param request:
        :return:
        """
        pass
