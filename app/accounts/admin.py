from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    fieldsets = ((None, {"fields": ("middle_name", "phone_number")}),) + UserAdmin.fieldsets
    add_fieldsets = (
        (None, {"fields": ("last_name", "first_name", "middle_name", "email")}),
    ) + UserAdmin.add_fieldsets
    list_display = ["first_name", "last_name", "date_joined", "is_active"]
    list_filter = ["first_name", "last_name", "date_joined"]


admin.site.register(CustomUser, CustomUserAdmin)
