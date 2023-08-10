from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users
from .forms import UserCreationForm,UserChangeForm
# Register your models here.
class CostumeUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    model = Users
    list_display=['email','is_superuser','is_active']
    list_filter=['email','is_superuser','is_active']
    search_fields=('email',)
    ordering=('email',)
    fieldsets = (
        ('Authentication', {
            "fields":(
                'email','password'
            ),
        }),
        ('permissions', {
            "fields":(
                'is_staff','is_active','is_superuser'
            ),
        }),
        ('group permissions', {
            "fields":(
                'groups','user_permissions'
            ),
        }),
        ('important date', {
            "fields":(
                'last_login',
            ),
        }),
    )
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )

admin.site.register(Users, CostumeUserAdmin)