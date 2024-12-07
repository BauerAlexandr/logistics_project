from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Bank, Cargo, Cargobatch, City, Client, Crew, Pier     
from .models import CustomUser, Port, Route, Service, Ship, Shiptype, Status, Street, Summary, Transportation, Unitofmeasurement
# Register your models here.

class CustomUserAdmin(UserAdmin):
    # Поля для отображения в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    # Поля для отображения в деталях пользователя
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'groups'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Bank)
admin.site.register(Cargo)
admin.site.register(Cargobatch)
admin.site.register(City)
admin.site.register(Client)
admin.site.register(Crew)
admin.site.register(Pier)
admin.site.register(Port)
admin.site.register(Route)
admin.site.register(Service)
admin.site.register(Ship)
admin.site.register(Shiptype)
admin.site.register(Status)
admin.site.register(Street)
admin.site.register(Summary)
admin.site.register(Transportation)
admin.site.register(Unitofmeasurement)
