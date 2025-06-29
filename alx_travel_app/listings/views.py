from django.shortcuts import render

# Create your views here.
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Booking, Payment

CHAPA_BASE_URL = "https://api.chapa.co/v1"

@api_view(['POST'])
def initiate_payment(request):
    booking_id = request.data.get("booking_id")
    booking = Booking.objects.get(id=booking_id)
    
    payload = {
        "amount": str(booking.listing.price),
        "currency": "ETB",
        "email": "user@example.com",  # Change this dynamically if needed
        "first_name": booking.customer_name,
        "tx_ref": f"chapa-{booking_id}",
        "callback_url": "http://yourdomain.com/payment/verify/",
        "return_url": "http://yourdomain.com/payment/success/",
        "customization[title]": "Booking Payment",
        "customization[description]": f"Payment for booking {booking.id}"
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.post(f"{CHAPA_BASE_URL}/transaction/initialize", json=payload, headers=headers)
    data = response.json()

    if response.status_code == 200 and data["status"] == "success":
        Payment.objects.create(
            booking=booking,
            transaction_id=data["data"]["tx_ref"],
            amount=booking.listing.price,
            status="Pending"
        )
        return Response(data["data"])  # contains the payment URL
    else:
        return Response({"error": "Failed to initiate payment"}, status=400)


@api_view(['GET'])
def verify_payment(request, tx_ref):
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.get(f"{CHAPA_BASE_URL}/transaction/verify/{tx_ref}", headers=headers)
    data = response.json()

    if response.status_code == 200 and data["status"] == "success":
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
            payment.status = "Completed"
            payment.save()
            return Response({"message": "Payment verified successfully"})
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)
    else:
        return Response({"error": "Verification failed"}, status=400)
