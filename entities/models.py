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

    def __str__(self):
        return self.attribute_set_name

    class Meta:
        verbose_name = 'Field Set'
        verbose_name_plural = 'Field Sets'


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
    parent_attribute_group = models.ForeignKey('AttributeGroup', on_delete=models.CASCADE, null=True, blank=True)
    conditional_display = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True)

    def __str__(self):
        return self.attribute_group_name + f" [{self.attribute_group_code}]"

    class Meta:
        verbose_name = 'Field Group'
        verbose_name_plural = 'Field Groups'


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

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name} [{self.email}]"


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
    role_code = models.CharField(max_length=55, unique=True)
    role_label = models.TextField()

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.role_label + f" [{self.role_code}]"


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

    class Meta:
        verbose_name = 'User - Role'
        verbose_name_plural = 'User - Roles'


"""
====================================================================================================
                                ### User Role Entity Tables ###  
====================================================================================================
"""


class UserRoleEntityDataTypes(models.Model):
    """
    Labeled as Section on the frontend
    User type = Generic
    Data types for the All role type records. Primary key records
    """
    entity_data_type_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    attribute_set_id = models.ForeignKey(
        AttributeSet,
        on_delete=models.PROTECT,
        verbose_name="Attribute Set",
        db_column="attribute_set_id"
    )
    data_type_code = models.CharField(max_length=55, unique=True)
    data_type_label = models.TextField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.data_type_label

    class Meta:
        verbose_name = 'User Section'
        verbose_name_plural = 'User Sections'


class UserRoleEntityData(models.Model):
    """
    User type = Generic.
    Each record - can be of personal info/visitor log/comm log/medical info/research questionnaire
    """
    entity_data_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    entity_data_type_id = models.ForeignKey(
        UserRoleEntityDataTypes,
        on_delete=models.CASCADE,
        verbose_name="role entity data type.",
        db_column="entity_data_type_id"
    )
    user_entity_id = models.ForeignKey(UserEntity, on_delete=models.CASCADE, verbose_name="User entity id",
                                       db_column="user_entity_id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "User Section Data"
        verbose_name_plural = "User Section Data"

    def __str__(self):
        return f"{self.user_entity_id.first_name} {self.user_entity_id.last_name} - {self.entity_data_type_id.data_type_label}"


class RolePermissions(models.Model):
    class RolePermissionOpTypes(models.TextChoices):
        """
        ENUM choices for role permission operation types
        """
        CREATE = 'CREATE', 'Create'
        EDIT = 'EDIT', 'Edit'
        DELETE = 'DELETE', 'Delete'
        VIEW = 'VIEW', 'View'

    permission_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    role_id = models.ForeignKey(
        Roles,
        on_delete=models.PROTECT,
        verbose_name="Role",
        db_column="role_id"
    )
    operation_type = models.CharField(choices=RolePermissionOpTypes.choices, max_length=10,
                                      default=RolePermissionOpTypes.CREATE, verbose_name="Operation")

    resource = models.ForeignKey(
        UserRoleEntityDataTypes,
        on_delete=models.PROTECT,
        verbose_name="Section",
        db_column="resource"
    )

    def __str__(self):
        return f"{self.role_id.role_label} - {self.operation_type.capitalize()} - {self.resource.data_type_label}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['role_id', 'operation_type', 'resource'],
                                    name='Unique Permission Group for: Role,Operation type and Resource')
        ]
        verbose_name = 'Role - Permission'
        verbose_name_plural = 'Role - Permissions'


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
    attribute_group = models.ForeignKey(
        AttributeGroup,
        on_delete=models.CASCADE,
        verbose_name="Attribute Group",
        db_column="attribute_group"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    sort_order = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.frontend_label} - [{self.attribute_code}] - [{self.attribute_type}]"

    class Meta:
        verbose_name = 'Field'
        verbose_name_plural = 'Fields'


class UserRoleAttributeOptionGroup(models.Model):
    """
    Option Group for Radio buttons or Select list.
    """
    group_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False, db_column="option_group_id")
    attribute = models.ForeignKey(
        UserRoleAttribute,
        on_delete=models.CASCADE,
        verbose_name="Field",
        db_column="attribute"
    )
    group_label = models.TextField()

    def __str__(self):
        return f"{self.group_label}"

    class Meta:
        verbose_name = "Field Option Group"
        verbose_name_plural = "Field Option Groups"


class UserRoleAttributeOptions(models.Model):
    """
    Options for Radio buttons or Select list.
    """
    option_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    option_label = models.TextField()
    option_code = models.TextField()
    option_group = models.ForeignKey(
        UserRoleAttributeOptionGroup,
        on_delete=models.CASCADE,
        verbose_name="Option Group",
        db_column="option_group",
        null=True
    )
    conditional_display_attribute_group = models.ForeignKey(
        AttributeGroup,
        on_delete=models.CASCADE,
        verbose_name="Conditional Attribute group",
        db_column="conditional_display_attribute_group",
        null=True
    )

    def __str__(self):
        return f"{self.option_label} - [{self.option_code}]"

    class Meta:
        verbose_name = "Field Option Value"
        verbose_name_plural = "Field Option Values"


class AttributeValues(models.Model):
    value_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    attribute = models.ForeignKey(
        UserRoleAttribute,
        on_delete=models.PROTECT,
        verbose_name="role entity attribute",
        db_column="attribute"
    )
    entity_data_id = models.ForeignKey(
        UserRoleEntityData,
        on_delete=models.CASCADE,
        verbose_name="role entity data",
        db_column="entity_data_id"
    )
    value_int = models.IntegerField(null=True)
    value_decimal = models.DecimalField(null=True, max_digits=9, decimal_places=4)
    value_time = models.TimeField(null=True)
    value_date = models.DateField(null=True)
    value_text = models.TextField(null=True)
    value_option = models.ForeignKey(
        UserRoleAttributeOptions,
        on_delete=models.CASCADE,
        verbose_name="option value",
        db_column="value_option",
        null=True
    )

    def __str__(self):
        return F"{self.entity_data_id.entity_data_type_id.data_type_label}  [{self.attribute.attribute_code}]"

    class Meta:
        verbose_name = "Field Value"
        verbose_name_plural = "Field Values"
