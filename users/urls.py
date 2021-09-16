from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import *

urlpatterns = [
    # GET/POST for roles
    path('roles/', RolesViews.RolesList.as_view()),

    # UPDATE/DELETE for roles
    path('roles/<str:role_id>', RolesViews.RolesDetail.as_view()),

    # List entity data types for role.
    path('roles/<str:role_id>/entity-data-types', RolesViews.RolesEntityDataTypeList.as_view()),
    path('roles/<str:role_id>/entity-data-types/attributes', RolesViews.RolesEntityDataTypeListAttributes.as_view()),

    # GET/POST for role permissions
    path('role-permissions/', RolesViews.RolePermissionList.as_view()),

    # UPDATE/DELETE for role permissions
    path('role-permissions/<str:role_permission_id>', RolesViews.RolePermissionDetail.as_view()),

    # List Role Permissions by Role ID
    path('role-permissions/role/<str:role_id>', RolesViews.RolePermissionListByRole.as_view()),

    path('users/', UsersList.as_view()),  # GET/POST for user roles
    path('users/<str:user_entity_id>', UsersDetail.as_view()),  # UPDATE/DELETE for user roles
]

urlpatterns = format_suffix_patterns(urlpatterns)
