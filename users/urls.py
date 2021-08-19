from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from .views import *

urlpatterns = [
    # GET/POST for roles
    path('roles/', Roles.RolesList.as_view()),
    # UPDATE/DELETE for roles
    path('roles/<int:role_id>', Roles.RolesDetail.as_view()),

    # GET/POST for role permissions
    path('role-permissions/', Roles.RolePermission.as_view()),
    # UPDATE/DELETE for role permissions
    path('role-permissions/<int:role_permission_id>', Roles.RolePermissionDetail.as_view()),

    path('users/', UsersList.as_view()),  # GET/POST for user roles
    path('users/<str:user_entity_id>', UsersDetail.as_view()),  # UPDATE/DELETE for user roles
]

urlpatterns = format_suffix_patterns(urlpatterns)
