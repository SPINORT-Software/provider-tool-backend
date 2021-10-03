from django.contrib import admin
from .models import CaseManagerUsers, DailyWorkLoad, ClientAssessment

admin.site.register(CaseManagerUsers)
admin.site.register(DailyWorkLoad)
admin.site.register(ClientAssessment)