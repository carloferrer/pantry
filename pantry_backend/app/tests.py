from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch

from datetime import datetime

from .models import Consumable

class TestConsumableMethods(TestCase):
    def setUp(self):
        Consumable.consumables.create(name='milk',expiry='2021-01-01')

    def test_get_human_date_expiry(self):
        milk = Consumable.consumables.get(name='milk')
        expiry_result = milk.get_human_date_expiry()
        expiry_expected = 'Jan. 1, 2021'
        self.assertEqual(expiry_result, expiry_expected)

    @patch('django.utils.timezone.now')
    def test_get_days_to_expiry(self, mock_now):
        mock_now.return_value = datetime(2020, 1, 1)
        milk = Consumable.consumables.get(name='milk')
        days_result = milk.get_days_to_expiry()
        days_expected = 366
        self.assertEqual(days_result, days_expected)


class TestConsumableQuerySetMethods(TestCase):
    get_queryset = Consumable.consumables.get_queryset

    def setUp(self):
        mock_consumables = [
            { 'name': 'milk', 'expiry': '2021-01-01' },
            { 'name': 'eggs', 'expiry': '2021-01-11' },
            { 'name': 'bread', 'expiry': '2021-01-21' },
        ]

        for mock_consumable in mock_consumables:
            Consumable.consumables.create(name=mock_consumable['name'], expiry=mock_consumable['expiry'])

    @patch('django.utils.timezone.now')
    def test_get_expires_in_days(self, mock_now):
        mock_now.return_value = datetime(2021, 1, 1)
        get_expires_in_days = self.get_queryset().get_expires_in_days

        test_assertions = [
            {
                'result': [ *get_expires_in_days(1) ],
                'expected': [ self.get_queryset().get(name='milk')
                ]
            },
            {
                'result': [ *get_expires_in_days(10) ],
                'expected': [ *self.get_queryset().filter(name__in=('milk', 'eggs')) ]
            },
            {
                'result': [ *get_expires_in_days(20) ],
                'expected': [ *self.get_queryset().filter(name__in=('milk', 'eggs', 'bread')) ]
            }
        ]

        for test_assertion in test_assertions:
            self.assertEqual(test_assertion['result'], test_assertion['expected'])

    @patch('django.utils.timezone.now')
    def test_get_expires_by_date(self, mock_now):
        mock_now.return_value = datetime(2021, 1, 1)
        get_expires_by_date = self.get_queryset().get_expires_by_date

        test_assertions = [
            {
                'result': [ *get_expires_by_date('2021-01-01') ],
                'expected': [ self.get_queryset().get(name='milk')
                ]
            },
            {
                'result': [ *get_expires_by_date('2021-01-11') ],
                'expected': [ *self.get_queryset().filter(name__in=('milk', 'eggs')) ]
            },
            {
                'result': [ *get_expires_by_date('2021-01-21') ],
                'expected': [ *self.get_queryset().filter(name__in=('milk', 'eggs', 'bread')) ]
            }
        ]

        for test_assertion in test_assertions:
            self.assertEqual(test_assertion['result'], test_assertion['expected'])
