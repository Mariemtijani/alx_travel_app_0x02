from django.db import models

# Create your models here.
from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    listing = models.ForeignKey(Listing, related_name="bookings", on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    booking_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.listing.title} by {self.customer_name}"


class Review(models.Model):
    listing = models.ForeignKey(Listing, related_name="reviews", on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.listing.title} by {self.customer_name}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, related_name='payments', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.booking.customer_name} - {self.status}"