from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .model import user_entity_data


class UserEntity(APIView):
    def __init__(self):
        self.user_entity_data = user_entity_data.UserEntityDataTypesModel()


class UserEntityDataTypesList(UserEntity):
    def post(self, request):
        """
        Add a user entity data type.
        :param request:
        :return:
        """
        try:
            response = self.user_entity_data.add_type(request.data)
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to add user entity data type.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        List all the user entity data types.
        :param request:
        :return:
        """
        try:
            response = self.user_entity_data.list_data_types()
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to fetch list of user entity data types'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserEntityDataTypesDetail(UserEntity):
    def get(self, request, type_id):
        """
        Get user entity data type detail.
        :param type_id:
        :param request:
        :return:
        """
        try:
            response = self.user_entity_data.get_type_detail(type_id)
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to fetch data type detail.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, type_id):
        """
        Update user entity data type detail.
        :param type_id:
        :param request:
        :return:
        """
        try:
            response = self.user_entity_data.update_type_detail(type_id, request.data)
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to update data type detail.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserEntityAttributes(UserEntity):
    pass


class UserEntityAttributeValues(UserEntity):
    pass
