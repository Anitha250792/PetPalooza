from django.contrib import admin
from .models import ContactMessage
from django.utils import timezone
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = ("ticket_id", "name", "email", "is_replied", "created_at")
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
        "is_replied",
    )

    def save_model(self, request, obj, form, change):

        # Only send email if admin entered reply and not already replied
        if obj.admin_reply and not obj.is_replied:

            try:
                message = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_emails=obj.email,
                    subject=f"Reply to your Ticket {obj.ticket_id}",
                    html_content=f"""
                        <h3>Petpalooza Support</h3>
                        <p><strong>Your Query:</strong></p>
                        <p>{obj.message}</p>
                        <hr>
                        <p><strong>Our Reply:</strong></p>
                        <p>{obj.admin_reply}</p>
                        <br>
                        <p>Thank you for contacting us ❤️</p>
                    """
                )

                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                sg.send(message)

                obj.is_replied = True
                obj.replied_at = timezone.now()

            except Exception as e:
                print("SendGrid Admin Reply Error:", e)

        super().save_model(request, obj, form, change)