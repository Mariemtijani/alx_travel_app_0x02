from django.core.management.base import BaseCommand
from listings.models import Listing

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        Listing.objects.create(
            title="Trip to Morocco",
            description="7 days tour in Marrakech and Sahara",
            price=999.99,
            available=True
        )

        Listing.objects.create(
            title="Paris Getaway",
            description="3 nights romantic trip in Paris",
            price=1499.99,
            available=True
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
