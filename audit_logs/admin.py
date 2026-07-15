from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "action",
        "module",
        "timestamp",
    )

    list_filter = (
        "action",
        "module",
    )