import requests
from django.conf import settings
from .models import Location, DistanceRecord
from django.core.exceptions import ObjectDoesNotExist


class LocationService:
    @staticmethod
    def geocode_address(address):
        """Geocode an address using Google Maps API."""
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={settings.GOOGLE_MAPS_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            results = response.json().get('results', [])
            if results:
                location_data = results[0]
                formatted_address = location_data['formatted_address']
                latitude = location_data['geometry']['location']['lat']
                longitude = location_data['geometry']['location']['lng']
                return formatted_address, latitude, longitude
            return None, None, None
        except requests.exceptions.RequestException as e:
            print(f"Error geocoding address {address}: {e}")
            return None, None, None

    @staticmethod
    def calculate_distance(start_lat, start_lng, end_lat, end_lng):
        """Calculate distance using Google Maps Distance Matrix API."""
        url = (
            f"https://maps.googleapis.com/maps/api/distancematrix/json?"
            f"origins={start_lat},{start_lng}&destinations={end_lat},{end_lng}&key={settings.GOOGLE_MAPS_API_KEY}"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            distance_data = response.json()
            distance_info = distance_data['rows'][0]['elements'][0]
            if distance_info['status'] == 'OK':
                return distance_info['distance']['value'] / 1000.0  # Convert to kilometers
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calculating distance: {e}")
            return None


class DistanceService:
    @staticmethod
    def get_or_create_location(name, address, lat, lng):
        location, created = Location.objects.get_or_create(
            name=name,
            defaults={
                'address': address,
                'latitude': lat,
                'longitude': lng
            }
        )
        return location

    @staticmethod
    def save_distance_record(start_location, end_location, distance_km):
        DistanceRecord.objects.create(
            start_location=start_location,
            end_location=end_location,
            distance_km=distance_km
        )
