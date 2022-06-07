import pandas as pd
from django.core.management import call_command
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from api.views import load_df


class TestDfEndpoints(TestCase):
    def setUp(self):
        call_command('load_data')
        self.client = APIClient()

    def test_load_df(self):
        df = load_df()
        self.assertIsInstance(df, pd.DataFrame)

    def test_average_age_per_industry(self):
        response = self.client.get(reverse('industry-age'))
        self.assertEqual(response.status_code, 200)

    def test_average_salary_per_industry(self):
        response = self.client.get(reverse('experience-salary'))
        self.assertEqual(response.status_code, 200)
