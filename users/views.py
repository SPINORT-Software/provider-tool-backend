from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .model import accounts, roles
from entities.models import UserEntity, Roles
from .serializers import UserSerailzier
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException

from datetime import datetime
from rest_framework import serializers


class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


class RolesViews:
    class RolesList(APIView, PageNumberPagination):
        """
        List all roles or create a role.
        """

        def __init__(self):
            self.roles_model = roles.RolesModel()

        def post(self, request):
            """
            Add a new role record.
            :param request:
            :return:
            """
            try:
                response = self.roles_model.create_role(request.data)
                return response.get_response()
            except Exception as e:
                return Response({
                    'result': False,
                    'message': 'Missing required request fields.'
                }, status=status.HTTP_400_BAD_REQUEST)

        def get(self, request):
            """
            Get all the role records.
            :param request:
            :return:
            """
            try:
                # response = self.roles_model.list_roles()
                # return response.get_response()
                users = [Comment(email='leila@example.com1', content='foo bar'),
                         Comment(email='leila@example.com2', content='foo bar'),
                         Comment(email='leila@example.com3', content='foo bar'),
                         Comment(email='leila@example.com4', content='foo bar'),
                         Comment(email='leila@example.com5', content='foo bar'),
                         Comment(email='leila@example.com6', content='foo bar'),
                         Comment(email='leila@example.com7', content='foo bar'),
                         Comment(email='leila@example.com8', content='foo bar')]

                # users = Roles.objects.all()
                results = self.paginate_queryset(users, request, view=self)
                serializer = CommentSerializer(results, many=True)
                # serializer = UserSerailzier.UserSerializer(results, many=True)
                return self.get_paginated_response({
                    'result': True,
                    'value': serializer.data
                })
            except APIException as e:
                return Response({
                    'result': False,
                    'message': 'Failed to fetch roles list.'
                }, status=status.HTTP_400_BAD_REQUEST)

    class RolesDetail(APIView):
        """
        API Class for Role Detail
        """

        def __init__(self):
            self.roles_model = roles.RolesModel()

        def get(self, request, role_id):
            try:
                response = self.roles_model.get_role_detail(role_id)
                return response.get_response()
            except Exception as e:
                return Response({
                    'result': False,
                    'message': "Could not fetch role details."
                }, status=status.HTTP_400_BAD_REQUEST)

        def put(self, request, role_id):
            """
            Update a role entity record.
            :param request:
            :return:
            """
            try:
                response = self.roles_model.update_role_detail(role_id, request.data)
                return response.get_response()
            except Exception as e:
                return Response({
                    'result': False,
                    'message': "Could not update role details."
                }, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, role_id):
            """
            Delete a role entity record.
            :param request:
            :return:
            """
            pass

    class RolePermissionList(APIView):
        """
        List all role permissions or create a role permission.
        """

        def __init__(self):
            self.role_permission_model = roles.RolesPermissionModel()

        def post(self, request):
            """
            Add a new role permission.
            :param request:
            :return:
            """
            try:
                response = self.role_permission_model.add_role_permission(request.data)
                return response.get_response()
            except Exception as e:
                return Response({
                    'result': False,
                    'message': 'Missing required request fields.'
                }, status=status.HTTP_400_BAD_REQUEST)

        def get(self, request):
            """
            Get all the role permissions.
            :param request:
            :return:
            """
            try:
                response = self.role_permission_model.list_role_permission()
                return response.get_response()
            except Exception as e:
                return Response({
                    'result': False,
                    'message': 'Missing required request fields.'
                }, status=status.HTTP_400_BAD_REQUEST)

    class RolePermissionDetail(APIView):
        """
        API Class for Role Permission Detail
        """

        def __init__(self):
            self.role_permission_model = roles.RolesPermissionModel()

        def get(self, request, role_permission_id):
            """
            Get role permission entity record detail.
            :param role_permission_id:
            :param request:
            :return:
            """
            try:
                response = self.role_permission_model.get_detail(role_permission_id)
                return response.get_response()
            except Exception as e:
                return Response({
                    'result': False,
                    'message': 'Missing required request fields.'
                }, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, role_permission_id):
            """
            Delete a role permission entity record.
            :param role_permission_id:
            :param request:
            :return:
            """
            try:
                response = self.role_permission_model.delete(role_permission_id)
                return response.get_response()
            except Exception as e:
                return Response({
                    'result': False,
                    'message': 'Failed to delete role permissions.'
                }, status=status.HTTP_400_BAD_REQUEST)

    class RolePermissionListByRole(APIView):
        def __init__(self):
            self.role_permission_model = roles.RolesPermissionModel()

        def get(self, request, role_id):
            """
            List all the role permissions by role.
            :param request:
            :return:
            """
            try:
                response = self.role_permission_model.list_role_permission_by_role(role_id)
                return response.get_response()
            except Exception as e:
                return Response({
                    'result': False,
                    'message': 'Missing required request fields.'
                }, status=status.HTTP_400_BAD_REQUEST)


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
