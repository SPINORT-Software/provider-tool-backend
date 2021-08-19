import datetime

from django.db import models
import uuid

"""
====================================================================================================
                                ### Attribute Set / Attribute Group / Entity Types / User Entity Types ###
====================================================================================================
"""


class AttributeSet(models.Model):
    attribute_set_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False,
                                        db_column="attribute_set_id")
    attribute_set_name = models.TextField()
    attribute_set_code = models.CharField(max_length=55, unique=True, null=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AttributeGroup(models.Model):
    attribute_group_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    attribute_set_id = models.ForeignKey(
        AttributeSet,
        on_delete=models.PROTECT,
        verbose_name="Attribute Set",
        db_column="attribute_set_id"
    )
    is_default_group = models.BooleanField(default=False)
    attribute_group_code = models.CharField(max_length=55, unique=True)
    attribute_group_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class EntityType(models.Model):
    """
    Entity Types for all entities across the system.
    """
    entity_type_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    entity_type_label = models.CharField(max_length=45)
    entity_type_code = models.CharField(max_length=45, unique=True)


class UserEntity(models.Model):
    """
    User Entity.
    Primary record of a user in the application (irrespective of the type of user)
    """
    user_entity_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=45, unique=True)
    password = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)


class EntityUpdates(models.Model):
    """
    Update Log to any entity across the system
    """
    entity_update_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    entity_id = models.CharField(max_length=32)
    entity_type_id = models.ForeignKey(
        EntityType,
        on_delete=models.PROTECT,
        verbose_name="Entity type",
        db_column="entity_type_id"
    )
    updated_at = models.DateTimeField()
    update_comments = models.TextField()
    updated_user_id = models.CharField(max_length=32)
    fields_updated = models.TextField()


"""
====================================================================================================
                    ### Generic Tables - Users / Roles / Role Permissions ###  
====================================================================================================
"""


class Roles(models.Model):
    role_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    role_code = models.TextField()
    role_label = models.TextField()


class UserRoles(models.Model):
    user_role_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user_entity_id = models.ForeignKey(
        UserEntity,
        on_delete=models.PROTECT,
        verbose_name="User ID",
        db_column="user_entity_id"
    )
    role_id = models.ForeignKey(
        Roles,
        on_delete=models.PROTECT,
        verbose_name="Role ID",
        db_column="role_id"
    )


class RolePermissions(models.Model):
    class RolePermissionOpTypes(models.TextChoices):
        """
        ENUM choices for role permission operation types
        """
        CREATE = 'CREATE', ('Create')
        EDIT = 'EDIT', ('Edit')
        DELETE = 'DELETE', ('Delete')

    permission_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    role_id = models.ForeignKey(
        Roles,
        on_delete=models.PROTECT,
        verbose_name="Role ID",
        db_column="role_id"
    )
    operation_id = models.CharField(choices=RolePermissionOpTypes.choices, max_length=10,
                                    default=RolePermissionOpTypes.CREATE)
    entity_type_id = models.ForeignKey(
        EntityType,
        on_delete=models.PROTECT,
        verbose_name="Entity Type",
        db_column="entity_type_id"
    )
    resource_entity_id = models.CharField(
        max_length=32)  # resource ID - entity ID of the record for all possible user types


"""
====================================================================================================
                                ### User Role Entity Tables ###  
====================================================================================================
"""


class UserRoleEntityDataTypes(models.Model):
    """
    User type = Generic
    Data types for the All role type records. Primary key records
    """
    entity_data_type_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    data_type_code = models.TextField()
    data_type_label = models.TextField()


class UserRoleEntityData(models.Model):
    """
    User type = Generic.
    Each record - can be of personal info/visitor log/comm log/medical info/research questionnaire
    """
    entity_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    entity_data_type_id = models.ForeignKey(
        UserRoleEntityDataTypes,
        on_delete=models.CASCADE,
        verbose_name="role entity data record type.",
        db_column="entity_data_type_id"
    )
    user_entity_id = models.ForeignKey(UserEntity, on_delete=models.CASCADE,
                                       verbose_name="User entity id", db_column="user_entity_id")
    attribute_set_id = models.ForeignKey(
        AttributeSet,
        on_delete=models.PROTECT,
        verbose_name="Attribute Set",
        db_column="attribute_set_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class UserRoleAttribute(models.Model):
    """
    Attributes for any user's entity data.
    """
    attribute_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    attribute_code = models.TextField()
    frontend_label = models.TextField()
    frontend_input = models.TextField()
    attribute_type = models.TextField()
    is_required = models.BooleanField()
    note = models.TextField()
    attribute_group_id = None


class UserRoleAttributeValues(models.Model):
    """
    Values for Attributes
    """
    value_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    attribute_id = models.ForeignKey(
        UserRoleAttribute,
        on_delete=models.PROTECT,
        verbose_name="role entity attribute",
        db_column="attribute_id"
    )
    entity_type_id = models.ForeignKey(
        EntityType,
        on_delete=models.PROTECT,
        verbose_name="role entity type",
        db_column="entity_type_id"
    )
    entity_id = models.ForeignKey(
        UserRoleEntityData,
        on_delete=models.PROTECT,
        verbose_name="role entity data ID",
        db_column="entity_id"
    )
    value = models.TextField()
