from django.test import TestCase
from unittest.mock import patch
from distance.services import LocationService, DistanceService
from distance.models import Location, DistanceRecord

class LocationServiceTest(TestCase):

    @patch('requests.get')
    def test_geocode_address(self, mock_get):
        mock_get.return_value.json.return_value = {
            'results': [{
                'formatted_address': "Test Address",
                'geometry': {
                    'location': {
                        'lat': 40.7128,
                        'lng': -74.0060
                    }
                }
            }]
        }
        formatted_address, lat, lng = LocationService.geocode_address("Test Location")
        self.assertEqual(formatted_address, "Test Address")
        self.assertEqual(lat, 40.7128)
        self.assertEqual(lng, -74.0060)

    @patch('requests.get')
    def test_calculate_distance(self, mock_get):
        mock_get.return_value.json.return_value = {
            'rows': [{
                'elements': [{
                    'status': 'OK',
                    'distance': {
                        'value': 3930000
                    }
                }]
            }]
        }
        distance_km = LocationService.calculate_distance(40.7128, -74.0060, 34.0522, -118.2437)
        self.assertEqual(distance_km, 3930.0)


class DistanceServiceTest(TestCase):

    def setUp(self):
        self.start_location = Location.objects.create(
            name="Start Location",
            address="Start Address",
            latitude=40.7128,
            longitude=-74.0060
        )
        self.end_location = Location.objects.create(
            name="End Location",
            address="End Address",
            latitude=34.0522,
            longitude=-118.2437
        )

    def test_get_or_create_location(self):
        location = DistanceService.get_or_create_location(
            "New Location", "New Address", 37.7749, -122.4194)
        self.assertEqual(location.name, "New Location")
        self.assertEqual(location.address, "New Address")

    def test_save_distance_record(self):
        DistanceService.save_distance_record(self.start_location, self.end_location, 3930.0)
        self.assertEqual(DistanceRecord.objects.count(), 1)
        record = DistanceRecord.objects.first()
        self.assertEqual(record.start_location, self.start_location)
        self.assertEqual(record.end_location, self.end_location)
        self.assertEqual(record.distance_km, 3930.0)
