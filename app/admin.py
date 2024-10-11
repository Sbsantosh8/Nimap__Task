from django.contrib import admin
from .models import Client, Project


class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "client_name", "created_at", "created_by")
    ordering = ("created_at",)
    readonly_fields = ("created_at",)
    raw_id_fields = ("created_by",)
    list_filter = ("created_at",)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "project_name", "client", "created_at", "created_by")
    ordering = ("created_at",)
    readonly_fields = ("created_at",)
    list_filter = ("client",)


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)


from django.contrib import admin
from .models import Project, Client


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "project_name", "get_client_name", "created_at", "created_by")
    ordering = ("created_at",)
    readonly_fields = ("created_at",)
    list_filter = ("client",)

    def get_client_name(self, obj):
        return obj.client.client_name if obj.client else None

    get_client_name.short_description = (
        "Client Name"  # This sets the column name in the admin
    )


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin list view
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


# Unregister the default User admin and register the custom User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
