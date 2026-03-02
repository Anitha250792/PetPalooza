from django.db import models
from django.utils import timezone
import uuid


class ContactMessage(models.Model):

    # 🔥 Auto-generated ticket ID
    ticket_id = models.CharField(max_length=50, unique=True)

    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()

    admin_reply = models.TextField(blank=True, null=True)
    is_replied = models.BooleanField(default=False)
    replied_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = "TKT-" + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id} - {self.name}"
    
class Review(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()   # 1 to 5
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name    
