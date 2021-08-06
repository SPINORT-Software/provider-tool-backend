from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from .views import *

urlpatterns = [
    path('users/', UserEntity.as_view()),  # GET/POST for users
    path('users/<int:user_id>', UserEntityDetail.as_view()),  # UPDATE/DELETE for users
    path('user-validate/', UserAccountValidate.as_view()),  # GET/POST for users

    path('roles/', Role.as_view()),  # GET/POST for roles
    path('roles/<int:role_id>', RoleDetail.as_view()),  # UPDATE/DELETE for roles

    path('role-permissions/', RolePermission.as_view()),  # GET/POST for role permissions
    path('role-permissions/<int:role_permission_id>', RolePermissionDetail.as_view()),
    # UPDATE/DELETE for role permissions

    path('user-roles/', UserRole.as_view()),  # GET/POST for user roles
    path('user-roles/<int:user_role_id>', UserRoleDetail.as_view()),  # UPDATE/DELETE for user roles

    path('case-managers', AccountEntity.as_view(), {'role': 'case-manager'}),
    # GET/POST for case manager entity records
    path('case-managers/<int:casemgr_id>', AccountEntityDetail.as_view(), {'role': 'case-manager'}),
    # UPDATE/DELETE for case manager entity records
]

urlpatterns = format_suffix_patterns(urlpatterns)
