"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime

from django.test import TestCase
from my_calendar.views import earlier_date
from django.test.client import Client


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class TimeTests(TestCase):
    def test_earlier_date(self):
        """ Tests that date1 is earler."""
        date1 = datetime(2013, 5, 20, 0, 0)
        date2 = datetime(2013, 6, 19, 0, 0)
        self.assertEqual(date1, earlier_date(date1, date2))
        self.assertEqual(date1, earlier_date(date2, date1))


class ClientTest(TestCase):
    def test_response(self):
        c = Client()
        response = c.post('login/')
        self.assertEqual(response.status_code, 200)
