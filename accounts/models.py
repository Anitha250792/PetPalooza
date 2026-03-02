from django.db import models
import uuid

class ContactMessage(models.Model):

    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Replied', 'Replied'),
    )

    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()

    admin_reply = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.ticket_id}"
    
class Review(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()   # 1 to 5
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name    
