from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

# admin.site.register(CustomUser)
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model=CustomUser
    fieldsets=(
        (None,{'fields':('username','password')}),
        ('Personal Info',{'fields':('first_name','last_name','email','phone_number','profile_image')}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important Dates',{'fields':('last_login','date_joined')}),
    )
    list_display=('username','email','first_name','last_name','is_staff')
    search_fields=('username','email','first_name','last_name')

