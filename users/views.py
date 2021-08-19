from django.shortcuts import render
from entities.models import UserEntity, UserRoleEntityData, \
    UserRoleAttribute, UserRoleAttributeValues, UserRoleEntityDataTypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .model import accounts


class Roles:
    class RolesList(APIView):
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

    class RolesDetail(APIView):
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


class UsersList(APIView):
    """
    List all user entity  or create a user entity for any type
    To create a case manager, client, clinician, paramedic and a research team member
    """

    def __init__(self):
        self.accounts_model = accounts.Accounts()

    def post(self, request):
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
            response = self.accounts_model.create_account(request.data)
            return response.get_response()
        except AttributeError:
            return Response({
                'result': False,
                'message': 'Missing required request fields.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        - Get all records from user type entity table.
        - List by pagination (Later)
        :param request:
        :return:
        """
        try:
            response = self.accounts_model.list_users()
            return response.get_response()
        except Exception:
            return Response({
                'result': False,
                'message': 'Failed to fetch list of users.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UsersDetail(APIView):
    accounts_model = accounts.Accounts()

    def get(self, request, user_entity_id):
        """
        Get Attribute Group detail
        :param request:
        :param attribute_group_id:
        :return:
        """
        try:
            response = UsersDetail.accounts_model.get_user_detail(user_entity_id)
            return response.get_response()
        except Exception:
            return Response({
                'result': False,
                'message': 'Failure to fetch User detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, user_entity_id):
        """
        Update the attribute group detail.
        :param request:
        :param attribute_group_id:
        :return:
        """
        try:
            response = UsersDetail.accounts_model.update_user_detail(user_entity_id, request.data)
            return response.get_response()
        except Exception as e:
            print(e)
            return Response({
                'result': False,
                'message': 'Failure to update user detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def delete(self, request, attribute_group_id):
    #     """
    #     Require additional permission/access to delete AttributeGroup record.
    #     :param attribute_set_id:
    #     :param request:
    #     :return:
    #     """
    #     try:
    #         response = attributeGroupModel.delete_attribute_group_detail(attribute_group_id)
    #         return response.get_response()
    #     except (Error, ValidationError):
    #         return Response({
    #             'result': False,
    #             'message': 'Could not delete attribute group detail.'
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
