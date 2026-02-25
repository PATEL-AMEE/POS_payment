from django.db import models

class Transaction(models.Model):
    METHOD_CHOICES = [
        ("card", "Card"),
        ("qr", "QR"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("declined", "Declined"),
        ("offline", "Offline"),
        ("expired", "Expired"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    reference = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    refund_reference = models.CharField(max_length=20, blank=True, default="")

    def __str__(self):
        return f"{self.method} £{self.amount} {self.status}"