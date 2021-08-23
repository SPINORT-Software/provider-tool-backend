ALLOWED_PERMISSION_RESOURCE_TYPES = ['entity_data', 'attribute_group']
ALLOWED_PERMISSION_OPERATION_TYPES = ['CREATE', 'DELETE', 'EDIT']

API_ROLE_CREATE_REQUEST_BODY = ["code", "label"]
API_ROLE_PERMISSION_CREATE_REQUEST_BODY = ["role_id", "operation_type", "resource_type", "resource_id"]

API_ENTITY_DATA_TYPES_CREATE_REQUEST_BODY = ["data_type_code", "data_type_label"]
API_ENTITY_DATA_TYPES_UPDATE_REQUEST_BODY = ["data_type_label", "is_active"]

API_ENTITY_ATTRIBUTE_CREATE_REQUEST_BODY = [
    "attribute_code",
    "attribute_type",
    "frontend_label",
    "frontend_input",
    "is_required",
    "note"
]
API_ENTITY_ATTRIBUTE_UPDATE_REQUEST_BODY = [
    "frontend_label",
    "is_required",
    "note",
    "is_active"
]
