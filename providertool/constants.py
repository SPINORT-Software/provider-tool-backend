ALLOWED_PERMISSION_RESOURCE_TYPES = ['entity_data', 'attribute_group']
ALLOWED_PERMISSION_OPERATION_TYPES = ['CREATE', 'DELETE', 'EDIT']

API_ROLE_CREATE_REQUEST_BODY = ["code", "label"]
API_ROLE_PERMISSION_CREATE_REQUEST_BODY = ["role_id", "operation_type", "resource_type", "resource_id"]

API_ENTITY_DATA_TYPES_CREATE_REQUEST_BODY = ["data_type_code", "data_type_label", "attribute_set"]
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

API_ENTITY_DATA_CREATE_REQUEST_BODY = ['data_type', 'user_id', 'attributes']
API_ENTITY_DATA_UPDATE_REQUEST_BODY = []

# Attributes
ATTRIBUTE_TYPE_DICT = {
    'number': 'value_int',
    'input_number': 'value_int',
    'decimal': 'value_decimal',
    'input_decimal': 'value_decimal',
    'time': 'value_time',
    'input_time': 'value_time',
    'date': 'value_date',
    'input_date': 'value_date',
    'text': 'value_text',
    'input_text': 'value_text'
}
