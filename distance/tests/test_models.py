from django.test import TestCase
from distance.models import Location, DistanceRecord

class LocationModelTest(TestCase):

    def setUp(self):
        self.location = Location.objects.create(
            name="Test Location",
            address="123 Test St",
            latitude=40.7128,
            longitude=-74.0060
        )

    def test_location_creation(self):
        self.assertEqual(self.location.name, "Test Location")
        self.assertEqual(self.location.address, "123 Test St")
        self.assertEqual(self.location.latitude, 40.7128)
        self.assertEqual(self.location.longitude, -74.0060)


class DistanceRecordModelTest(TestCase):

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
        self.distance_record = DistanceRecord.objects.create(
            start_location=self.start_location,
            end_location=self.end_location,
            distance_km=3930.0
        )

    def test_distance_record_creation(self):
        self.assertEqual(self.distance_record.start_location, self.start_location)
        self.assertEqual(self.distance_record.end_location, self.end_location)
        self.assertEqual(self.distance_record.distance_km, 3930.0)
