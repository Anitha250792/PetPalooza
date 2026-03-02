from django.contrib import admin
from .models import ContactMessage
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "ticket_id",
        "name",
        "email",
        "subject",
        "status",
        "created_at",
    )

    list_filter = ("status", "created_at")
    search_fields = ("ticket_id", "name", "email", "subject")

    readonly_fields = (
        "ticket_id",
        "name",
        "email",
        "subject",
        "message",
        "created_at",
    )

    fields = (
        "ticket_id",
        "name",
        "email",
        "subject",
        "message",
        "admin_reply",
        "status",
    )

    def save_model(self, request, obj, form, change):

        # If admin wrote reply AND status is not already resolved
        if obj.admin_reply and obj.status != "Resolved":

            send_mail(
                subject=f"Reply to your Ticket {obj.ticket_id}",
                message=obj.admin_reply,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.email],
                fail_silently=False,
            )

            obj.status = "Resolved"

        super().save_model(request, obj, form, change)