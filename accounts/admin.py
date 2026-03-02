from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import ContactMessage
from django.conf import settings


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = ("ticket_id", "name", "email", "subject", "is_replied", "created_at")
    readonly_fields = ("ticket_id", "name", "email", "subject", "message", "created_at")

    fields = (
        "ticket_id",
        "name",
        "email",
        "subject",
        "message",
        "admin_reply",
        "is_replied",
        "replied_at",
    )

    def save_model(self, request, obj, form, change):

        # Only send email if reply added AND not already replied
        if obj.admin_reply and not obj.is_replied:
            
            
            print("EMAIL BACKEND:", settings.EMAIL_BACKEND)
            print("SENDGRID KEY:", settings.SENDGRID_API_KEY)

            send_mail(
                subject=f"Reply to your Ticket {obj.ticket_id}",
                message=obj.admin_reply,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.email],
                fail_silently=False,
            )

            obj.is_replied = True
            obj.replied_at = timezone.now()

        super().save_model(request, obj, form, change)