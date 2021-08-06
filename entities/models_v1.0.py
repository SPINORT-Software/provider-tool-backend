from django.db import models
import uuid

"""
====================================================================================================
                                ### Attribute Set / Attribute Group / Entity Types / User Entity Types ###
====================================================================================================
"""


class AttributeSet(models.Model):
    attribute_set_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute_set_name = models.TextField()


class AttributeGroup(models.Model):
    attribute_group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute_set_id = models.ForeignKey(
        AttributeSet,
        on_delete=models.PROTECT,
        verbose_name="Attribute Set",
        db_column="attribute_set_id"
    )
    attribute_group_code = models.TextField()
    attribute_group_name = models.TextField()


class EntityType(models.Model):
    """
    Entity Types for all entities across the system.
    """
    entity_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type_label = models.CharField(max_length=45)
    entity_type_code = models.CharField(max_length=45, unique=True)


class UserEntity(models.Model):
    """
    User Entity.
    Primary record of a user in the application (irrespective of the type of user)
    """
    user_entity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute_set_id = models.ForeignKey(
        AttributeSet,
        on_delete=models.PROTECT,
        verbose_name="Attribute Set",
        db_column="attribute_set_id"
    )
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
    entity_update_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_code = models.TextField()
    role_label = models.TextField()


class UserRoles(models.Model):
    user_role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    permission_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
                                ### Client Entity Tables ###  
====================================================================================================
"""


class UserClientEntityDataTypes(models.Model):
    """
    User type = Client.
    Data types for the Client records. Primaru key records
    """
    entity_data_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_type_code = models.TextField()

    class ClientEntityDataTypes(models.TextChoices):
        """
        ENUM choices for client data record types
        """
        PERSONALINFO = 'PI', ('Personal Info')
        VISITORLOG = 'VL', ('Visitor Log')
        COMMUNICATIONLOG = 'CL', ('Communication Log')
        MEDICALINFO = 'MI', ('Medical Info')
        RESEARCHQ = 'RQ', ('Research Questionnaire')

    data_type_label = models.CharField(max_length=10, choices=ClientEntityDataTypes.choices,
                                       default=ClientEntityDataTypes.PERSONALINFO)


class UserClientEntityData(models.Model):
    """
    User type = Client.
    Each record is of a client - can be of personal info/visitor log/comm log/medical info/research questionnaire
    """
    entity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_data_type_id = models.ForeignKey(
        UserClientEntityDataTypes,
        on_delete=models.CASCADE,
        verbose_name="Client entity data record type.",
        db_column="entity_data_type_id"
    )
    user_entity_id = models.ForeignKey(UserEntity, on_delete=models.CASCADE,
                                       verbose_name="Client Personal Info Record", db_column="user_entity_id")
    attribute_set_id = models.ForeignKey(
        AttributeSet,
        on_delete=models.PROTECT,
        verbose_name="Attribute Set",
        db_column="attribute_set_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class UserClientAttribute(models.Model):
    """
    User type = Client.
    Attributes for any Client data.
    """
    attribute_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute_code = models.TextField()
    frontend_label = models.TextField()
    frontend_input = models.TextField()
    attribute_type = models.TextField()
    is_required = models.BooleanField()
    note = models.TextField()
    attribute_group_id = None


class UserClientAttributeValues(models.Model):
    """
    User type = Client.
    Values for the Client Attributes
    """
    value_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute_id = models.ForeignKey(
        UserClientAttribute,
        on_delete=models.PROTECT,
        verbose_name="client entity attribute",
        db_column="attribute_id"
    )
    entity_type_id = models.ForeignKey(
        EntityType,
        on_delete=models.PROTECT,
        verbose_name="client entity type",
        db_column="entity_type_id"
    )
    entity_id = models.ForeignKey(
        UserClientEntityData,
        on_delete=models.PROTECT,
        verbose_name="client entity data ID",
        db_column="entity_id"
    )
    value = models.TextField()


"""
====================================================================================================
                                ### Case Manager Entity Tables ###  
====================================================================================================
"""


class UserCaseMgrEntityDataTypes(models.Model):
    """
    User type = Case Manager.
    Data types for the Case Manager records. Primary key records
    """

    class CaseMgrEntityDataTypes(models.TextChoices):
        """
        ENUM choices for case mgr data record types
        """
        AGENDA = 'AGN', ('Agenda')
        REFERRAL = 'REF', ('Referral')
        ASSESSMENTREFERRAL = 'AR', ('Assessment Referral')
        FOLLOWUPACT = 'FUA', ('Follow Up Activities')
        RESEARCHQ = 'RQ', ('Research Questionnaire')

    entity_data_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_type_code = models.TextField()
    data_type_label = models.CharField(max_length=10, choices=CaseMgrEntityDataTypes.choices,
                                       default=CaseMgrEntityDataTypes.AGENDA)


class UserCaseMgrEntityData(models.Model):
    """
    User type = Case Manager.
    Each record of a Case Manager - can be of agenda/referral/assessment referral/follow up activity/research questionnaire
    """
    entity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_data_type_id = models.ForeignKey(
        UserCaseMgrEntityDataTypes,
        on_delete=models.CASCADE,
        verbose_name="case manager entity data record type.",
        db_column="entity_data_type_id"
    )
    user_entity_id = models.ForeignKey(UserEntity, on_delete=models.CASCADE,
                                       verbose_name="Client Personal Info Record", db_column="user_entity_id")
    attribute_set_id = models.ForeignKey(
        AttributeSet,
        on_delete=models.PROTECT,
        verbose_name="Attribute Set",
        db_column="attribute_set_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class UserCaseMgrAttribute(models.Model):
    """
    User type = Case Manager.
    Attributes for any case manager data.
    """
    attribute_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute_code = models.TextField()
    frontend_label = models.TextField()
    frontend_input = models.TextField()
    attribute_type = models.TextField()
    is_required = models.BooleanField()
    note = models.TextField()
    attribute_group_id = None


class UserCaseMgrAttributeValues(models.Model):
    """
    User type = Case Manager.
    Values for the Case Manager Attributes
    """
    value_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute_id = models.ForeignKey(
        UserCaseMgrAttribute,
        on_delete=models.PROTECT,
        verbose_name="case manager entity attribute",
        db_column="attribute_id"
    )
    entity_type_id = models.ForeignKey(
        EntityType,
        on_delete=models.PROTECT,
        verbose_name="case manager entity type",
        db_column="entity_type_id"
    )
    entity_id = models.ForeignKey(
        UserClientEntityData,
        on_delete=models.PROTECT,
        verbose_name="case manager entity data ID",
        db_column="entity_id"
    )
    value = models.TextField()
