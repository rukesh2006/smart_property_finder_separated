from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .models import EmailOTP

class OTPModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        
    def test_otp_creation_and_expiration(self):
        # Generate an OTP
        otp_record = EmailOTP.objects.create(user=self.user, otp='123456')
        
        # Verify fields
        self.assertEqual(otp_record.user, self.user)
        self.assertEqual(otp_record.otp, '123456')
        self.assertFalse(otp_record.is_verified)
        self.assertFalse(otp_record.is_expired())
        
        # Simulate time passage of 6 minutes (beyond 5 minute limit)
        otp_record.created_at = timezone.now() - datetime.timedelta(minutes=6)
        otp_record.save()
        
        # Verify expiration behavior
        self.assertTrue(otp_record.is_expired())
