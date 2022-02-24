from django.contrib import admin
from .models import User, ApplicationUser

# Register your models here.
admin.site.register(User)
admin.site.register(ApplicationUser)