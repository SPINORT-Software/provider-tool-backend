from django.contrib import admin
from .models import CaseManagerUsers, DailyWorkLoad, CaseManagerClientAssessment

admin.site.register(CaseManagerUsers)
admin.site.register(DailyWorkLoad)
admin.site.register(CaseManagerClientAssessment)