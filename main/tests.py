from django.test import TestCase
from django.urls import reverse
from .models import Porada

class ApiTesty(TestCase):
    def setUp(self):
        Porada.objects.create(tekst="Testowa porada", kategoria="motywacja")

    def test_losowa_porada(self):
        url = reverse('api_losowa_porada')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertIn('porada', r.json())
