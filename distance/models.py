from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=['name']),  # Indexing for faster lookups
            models.Index(fields=['latitude', 'longitude']),
        ]

    def __str__(self):
        return self.name

class DistanceRecord(models.Model):
    start_location = models.ForeignKey(Location, related_name='start_location', on_delete=models.CASCADE)
    end_location = models.ForeignKey(Location, related_name='end_location', on_delete=models.CASCADE)
    distance_km = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)  # Add timestamps for data tracking

    class Meta:
        indexes = [
            models.Index(fields=['start_location', 'end_location']),  # Indexing for faster queries
        ]

    def __str__(self):
        return f"{self.start_location} to {self.end_location} - {self.distance_km} km"
