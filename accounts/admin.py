from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import ContactMessage


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
    )

    def save_model(self, request, obj, form, change):

        # Only send if admin_reply added now
        if change:
            old_obj = ContactMessage.objects.get(pk=obj.pk)

            if not old_obj.admin_reply and obj.admin_reply:
                print("🔥 SENDING EMAIL")
                print("BACKEND:", settings.EMAIL_BACKEND)

                send_mail(
                    subject=f"Reply to your Ticket {obj.ticket_id}",
                    message=f"""
Hello {obj.name},

Your support ticket has been replied.

Admin Reply:
{obj.admin_reply}

Thank you,
PetPalooza Support
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.email],
                    fail_silently=False,
                )

                obj.is_replied = True
                obj.replied_at = timezone.now()

        super().save_model(request, obj, form, change)