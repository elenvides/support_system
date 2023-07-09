from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["groups", "user_permissions", "password"]
    readonly_fields = [
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
    ]
    list_filter = ["is_active", "role"]
    list_display = ["email", "first_name", "last_name", "role", "is_active"]
    search_fields = ["email", "last_name"]

    def get_readonly_fields(self, request, obj=None):
        # if obj not None, obj exists, so "email" is only for reading
        if obj:
            return self.readonly_fields + ["email"]
        return self.readonly_fields
