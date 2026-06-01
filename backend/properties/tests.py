from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Property


class SellerPropertyUpdateTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='seller1', password='pass12345')
        self.other_seller = User.objects.create_user(username='seller2', password='pass12345')
        self.property = Property.objects.create(
            owner=self.owner,
            title='Original Home',
            description='Original description',
            price='4500000.00',
            location='Hyderabad',
            property_type='apartment',
            listing_type='buy',
            bedrooms=2,
            bathrooms=2,
            area_sqft=1200,
            approval_status='approved',
        )

    def property_payload(self, **overrides):
        payload = {
            'title': 'Updated Home',
            'description': 'Updated description',
            'price': '4600000.00',
            'location': 'Bengaluru',
            'property_type': 'house',
            'listing_type': 'rent',
            'bedrooms': 3,
            'bathrooms': 2,
            'area_sqft': 1350,
            'amenities': 'parking, balcony',
            'status': 'available',
        }
        payload.update(overrides)
        return payload

    def test_owner_can_update_own_property(self):
        self.client.login(username='seller1', password='pass12345')

        response = self.client.post(
            reverse('property_update', args=[self.property.pk]),
            self.property_payload(),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('property_detail', args=[self.property.pk]))
        self.property.refresh_from_db()
        self.assertEqual(self.property.title, 'Updated Home')
        self.assertEqual(self.property.owner, self.owner)
        self.assertEqual(self.property.approval_status, 'pending')

    def test_other_seller_cannot_update_property(self):
        self.client.login(username='seller2', password='pass12345')

        response = self.client.post(
            reverse('property_update', args=[self.property.pk]),
            self.property_payload(title='Bad Update'),
        )

        self.assertEqual(response.status_code, 403)
        self.property.refresh_from_db()
        self.assertEqual(self.property.title, 'Original Home')
