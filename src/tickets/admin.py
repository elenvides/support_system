from django.contrib import admin

from tickets.models import Message, Ticket


class MessageInline(admin.TabularInline):
    model = Message
    fields = ["id", "text", "user", "timestamp"]
    readonly_fields = ["id", "text", "user", "timestamp"]
    extra = 0
    can_delete = False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = [MessageInline]

    list_display = ["id", "title", "user", "manager", "status"]
    list_filter = ["status"]
    search_fields = [
        "id",
        "title",
        "user__email",
        "user__last_name",
        "manager__email",
        "manager__last_name",
    ]
    readonly_fields = ["id", "title", "text", "user"]
    ordering = ["-id"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "user", "ticket", "timestamp"]
    list_filter = ["ticket"]
    search_fields = ["id", "text", "user__email", "user__last_name", "ticket__title"]
    readonly_fields = ["id", "text", "user", "ticket", "timestamp"]
    ordering = ["-timestamp"]
