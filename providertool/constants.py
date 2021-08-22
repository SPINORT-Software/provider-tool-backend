ALLOWED_PERMISSION_RESOURCE_TYPES = ['entity_data', 'attribute_group']
ALLOWED_PERMISSION_OPERATION_TYPES = ['CREATE', 'DELETE', 'EDIT']

API_ROLE_CREATE_REQUEST_BODY = ["code", "label"]
API_ROLE_PERMISSION_CREATE_REQUEST_BODY = ["role_id", "operation_type", "resource_type", "resource_id"]
