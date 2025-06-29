# ALX Travel App - 0x00

## Project Overview

This project implements:

- Django models for `Listing`, `Booking`, and `Review`
- Django REST Framework serializers
- Database seeding using Django management commands
- Swagger API documentation
- MySQL database integration using `django-environ`

---

## Models

### Listing
- `title` (CharField)
- `description` (TextField)
- `price` (DecimalField)
- `available` (BooleanField)

### Booking
- `listing` (ForeignKey to Listing)
- `customer_name` (CharField)
- `booking_date` (DateField)
- `created_at` (DateTimeField auto-generated)

### Review
- `listing` (ForeignKey to Listing)
- `customer_name` (CharField)
- `rating` (IntegerField)
- `comment` (TextField)
- `created_at` (DateTimeField auto-generated)

---

## Serializers

- `ListingSerializer`
- `BookingSerializer`

Both serializers are located in `listings/serializers.py`.

---

## Database Seeder

A management command `seed` is implemented to populate the database with sample `Listing` data.

- File: `listings/management/commands/seed.py`

To run the seed:

```bash
python manage.py seed
