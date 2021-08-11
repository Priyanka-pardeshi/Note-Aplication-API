from django.contrib import admin
from registerapp.models import Registration
# Register your models here.
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'password', 'contact', 'dob']

admin.site.register(Registration,RegistrationAdmin)