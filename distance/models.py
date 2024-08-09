# models.py
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    search_vector = SearchVectorField(null=True)  # Full-text search vector

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['latitude', 'longitude']),
            GinIndex(fields=['search_vector']),  # GIN index for full-text search
        ]

    def __str__(self):
        return self.name


class DistanceRecord(models.Model):
    start_location = models.ForeignKey(Location, related_name='start_location', on_delete=models.CASCADE)
    end_location = models.ForeignKey(Location, related_name='end_location', on_delete=models.CASCADE)
    distance_km = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_location', 'end_location']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.start_location} to {self.end_location} - {self.distance_km} km"
