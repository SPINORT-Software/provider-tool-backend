from rest_framework.response import Response
from entities.helper import HttpResponse
from rest_framework import status
from entities.models import UserEntity
from django.db.utils import IntegrityError, DatabaseError, Error


class Accounts:
    """
    Perform all Account CRUD operations.
    CRUD on users / types of user records.
    """

    def create_account(self, user_data, role):
        """
        Create a user account + a role type account (client/case manager/clinician/paramedic/research member)
        :param role:
        :param user_data:
        :param role:
        :return:
        """
        user_entity_result, user_entity_message, user_id = self.create_user_entity(user_data)
        if not user_entity_result:
            return HttpResponse(result=user_entity_result, message=user_entity_message, id="user_id", id_value=user_id,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            user_type_result, user_type_message, user_type_entity_id = self.create_user_type_entity(user_data, user_id)
            if not user_type_result:
                return HttpResponse(result=user_type_result, message=user_type_message, id="user_type_id",
                                    id_value=user_type_entity_id,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                user_role_result, user_role_message, user_role_id = self.create_user_role_entity(user_id)

                if not user_role_result:
                    return HttpResponse(result=user_type_result, message=user_type_message, id="user_type_id",
                                        id_value=user_type_entity_id,
                                        status=status.HTTP_400_BAD_REQUEST)

        # success response - return user_id
        return HttpResponse(result=True, message="Account creation success.", status=status.HTTP_200_OK, id="User ID",
                            id_value=user_id)

    def create_user_entity(self, user_data):
        """
        Create a user entity record.
        :param user_data:
        :return:
        """
        try:
            user_entity_created = UserEntity()
            user_entity_created.email = user_data.get("email")
            user_entity_created.first_name = user_data.get("firstname")
            user_entity_created.last_name = user_data.get("lastname")
            user_entity_created.password = user_data.get("password")
            user_entity_created.save()
            return True, "User entity created.", user_entity_created.user_entity_id
        except Error as e:
            # Log - e as error
            return False, "Could not create user.", None

    def create_user_type_entity(self, user_data, user_id):
        """
        Create a type entity record - client/case manager/clinician/paramedic/research member
        :param user_id:
        :param user_data:
        :return:
        """
        try:
            user_entity_created = UserEntity()
            user_entity_created.email = user_data.get("email")
            user_entity_created.save()
            return True, "User entity created.", user_entity_created.user_entity_id
        except Error as e:
            # Log - e as error
            return False, "Could not create user.", None

    def create_user_role_entity(self, user_entity_id):
        """
        Create user role record with user_entity_id and role_id.
        Return user_role_id.
        :param user_data:
        :return:
        """
        pass
