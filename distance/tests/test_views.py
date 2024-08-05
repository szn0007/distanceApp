from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

class DistanceViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('distance.services.LocationService.geocode_address')
    @patch('distance.services.LocationService.calculate_distance')
    def test_calculate_distance_view(self, mock_calculate_distance, mock_geocode_address):
        # Mock responses for geocode and distance calculation
        mock_geocode_address.side_effect = [
            ("Start Address", 40.7128, -74.0060),
            ("End Address", 34.0522, -118.2437)
        ]
        mock_calculate_distance.return_value = 3930.0

        response = self.client.get(reverse('calculate_distance'), {
            'start': 'Start Location',
            'end': 'End Location'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'start_address': "Start Address",
            'end_address': "End Address",
            'distance_km': 3930.0
        })

    def test_calculate_distance_view_invalid(self):
        # Test missing parameters
        response = self.client.get(reverse('calculate_distance'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Please provide both start and end addresses.'})

        response = self.client.get(reverse('calculate_distance'), {'start': 'Start Location'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Please provide both start and end addresses.'})

        response = self.client.get(reverse('calculate_distance'), {'end': 'End Location'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Please provide both start and end addresses.'})
