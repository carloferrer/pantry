from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch

from datetime import datetime

from .models import Consumable

class TestConsumableMethods(TestCase):
    def setUp(self):
        Consumable.objects.create(
            name="milk",
            expiry="2021-01-01",
        )

    def test_get_human_date_expiry(self):
        milk = Consumable.objects.get(name="milk")
        expiry_result = milk.get_human_date_expiry()
        expiry_expected = "Jan. 1, 2021"
        self.assertEqual(expiry_result, expiry_expected)

    @patch('django.utils.timezone.now')
    def test_get_days_to_expiry(self, mock_now):
        mock_now.return_value = datetime(2020, 1, 1)
        milk = Consumable.objects.get(name="milk")
        days_result = milk.get_days_to_expiry()
        days_expected = 366
        self.assertEqual(days_result, days_expected)
