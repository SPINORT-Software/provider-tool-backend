from django.db import migrations


def add_document_types(apps, schema_editor):
    DocumentTypes = apps.get_model('documents', 'DocumentTypes')

    document_types_list = [
        ('Referral Form', 'TYPE_REVIEW_BOARD_REFERRAL'),
        ('Assessment Form', 'TYPE_CASE_MANAGER_ASSESSMENT'),
        ('Provider Specific Assessment Form', 'TYPE_CASE_MANAGER_ASSESSMENT_PROVIDER_SPECIFIC_FORM'),
        ('Intervention Form', 'TYPE_CASE_MANAGER_INTERVENTION')
    ]

    for document_type in document_types_list:
        type_label = document_type[0]
        type_code = document_type[1]

        document_type_instance = DocumentTypes(type_label=type_label, type_code=type_code)
        document_type_instance.save()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_document_types),
    ]
