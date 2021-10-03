# from rest_framework.response import Response
# from entities.helper import HttpResponse
# from rest_framework import status
# from entities.models import UserEntity, UserRoles, Roles
# from django.db.utils import IntegrityError, DatabaseError, Error
# from django.contrib.auth.hashers import make_password
# from django.core.exceptions import ValidationError
#
#
# class Accounts:
#     """
#     Perform all Account CRUD operations.
#     CRUD on users / types of user records.
#     """
#
#     def __check_if_role_valid(self, role_data):
#         try:
#             return Roles.objects.get(role_id=role_data.get("type"))
#         except (Roles.DoesNotExist, ValidationError):
#             return False
#
#     def create_account(self, user_data):
#         """
#         Create a user account + a role type account (client/case manager/clinician/paramedic/research member)
#         :param user_data: User account credentials + role details.
#         :return:
#         """
#         # Missing required user fields
#         if "user" not in user_data or "role" not in user_data:
#             return HttpResponse(result=False, message="Missing required request field values.",
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         role_data = user_data.get('role')
#         if not self.__check_if_role_valid(role_data):
#             return HttpResponse(result=False,
#                                 message="Failure to create user role record. Invalid role value provided.",
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         user_entity_result, user_entity_message, user_entity_id = self.__create_user_entity(user_data)
#         if not user_entity_result:
#             return HttpResponse(result=user_entity_result, message=user_entity_message,
#                                 status=status.HTTP_400_BAD_REQUEST)
#         else:
#
#             user_role_result, user_role_message, user_role_id = self.__create_user_role_entity(user_entity_id,
#                                                                                                role_data)
#             if not user_role_result:
#                 return HttpResponse(result=user_role_result, message=user_role_message,
#                                     status=status.HTTP_400_BAD_REQUEST)
#
#         # success response - return user_id
#         return HttpResponse(result=True, message="Account creation success.", status=status.HTTP_200_OK, id="User ID",
#                             id_value=user_entity_id)
#
#     def __create_user_entity(self, user_data):
#         """
#         Create a user entity record.
#         :param user_data:
#         :return:
#         """
#         try:
#             user = user_data.get('user')
#             if all(key not in user for key in ("password", "firstname", "lastname", "email")):
#                 return False, "Missing required request field values in the key - 'user'", None
#             user_entity_created = UserEntity()
#             user_entity_created.email = user.get("email")
#             user_entity_created.first_name = user.get("firstname")
#             user_entity_created.last_name = user.get("lastname")
#             user_entity_created.password = make_password(user.get("password"))
#             user_entity_created.save()
#             return True, "User record created.", user_entity_created.user_entity_id
#         except IntegrityError as ie:
#             ie_message = ie.args[1]
#             if "Duplicate entry" in ie_message:
#                 ie_message = "The email address already exists. Could not create account."
#             return False, ie_message, None
#
#         except Error as e:
#             return False, "Failed to create user.", None
#
#     def __create_user_role_entity(self, user_entity_id, role_data):
#         """
#         Create user role record with user_entity_id and role_id.
#         Return user_role_id.
#         :param user_data:
#         :return:
#         """
#         try:
#             if "type" not in role_data:
#                 return False, "Missing required request field values in the key - 'role'", None
#
#             user_role_entity_created = UserRoles()
#             user_role_entity_created.role_id = Roles.objects.get(role_id=role_data.get("type"))
#             user_role_entity_created.user_entity_id = UserEntity.objects.get(user_entity_id=user_entity_id)
#             user_role_entity_created.save()
#             return True, "User role record creation success.", user_role_entity_created.user_role_id
#         except Roles.DoesNotExist:
#             return False, "Could not map Role. Please provide a valid role type value.", None
#         except UserEntity.DoesNotExist:
#             return False, "Failure to map the user to role provided. Please try creating the user account again.", None
#         except ValidationError:
#             return False, "Failure to create user role record. Invalid role value provided.", None
#         except Error as e:
#             return False, "Failed to create a role record for the user entity. ", None
#
#     def list_users(self):
#         """
#         List all UserEntity records.
#         :return:
#         """
#         try:
#             response_json = UserEntity.objects.values()
#
#             if len(response_json) > 0:
#                 return HttpResponse(result=True, message="Users list generated successfully.",
#                                     status=status.HTTP_200_OK,
#                                     value=response_json)
#             return HttpResponse(result=True, message="Could not find user records.",
#                                 status=status.HTTP_200_OK)
#         except Error as e:
#             return HttpResponse(result=False, message="Failure to list Users.",
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def get_user_detail(self, user_entity_id):
#         """
#         Get UserEntity detail.
#         :param user_entity_id:
#         :return:
#         """
#         try:
#             response_json = UserEntity.objects.values().get(user_entity_id=user_entity_id)
#             return HttpResponse(result=True, message="User detail fetch success.", status=status.HTTP_200_OK,
#                                 value=response_json)
#         except ValidationError:
#             return HttpResponse(result=False, message="Invalid user query parameter provided.",
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except UserEntity.DoesNotExist as e:
#             return HttpResponse(result=False, message="Could not find User detail.",
#                                 status=status.HTTP_200_OK)
#         except Error as e:
#             return HttpResponse(result=False, message="Failure to fetch User detail.",
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def update_user_detail(self, user_entity_id, user_data):
#         try:
#             update_user = UserEntity.objects.get(user_entity_id=user_entity_id)
#
#             if "user" in user_data:
#                 for attr, val in user_data['user'].items():
#                     if attr == "password":
#                         val = make_password(val)
#                     setattr(update_user, attr, val)
#
#                 update_user.save()
#                 return HttpResponse(result=True, message="User detail update success.", status=status.HTTP_200_OK)
#             else:
#                 return HttpResponse(result=False, message="Nothing to update.",
#                                     status=status.HTTP_200_OK)
#         except Error as e:
#             return HttpResponse(result=False, message="Failure to update user detail.",
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     # def delete_entity_type_detail(self, entity_type_id):
#     #     try:
#     #         EntityType.objects.get(entity_type_id=entity_type_id).delete()
#     #         return HttpResponse(result=True, message="Entity Type delete success.", status=status.HTTP_200_OK)
#     #     except (Error, EntityType.DoesNotExist) as e:
#     #         return HttpResponse(result=False, message="Could not delete Entity Type detail.",
#     #                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
