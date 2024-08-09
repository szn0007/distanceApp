from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Location
from .services import LocationService, DistanceService
from datetime import datetime
from django.core.cache import cache
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.postgres.search import TrigramSimilarity

def sanitize_input(input_str):
    """
    sanitize user input for more effective matching.
    """
    return input_str.strip().lower()

@require_GET
def calculate_distance(request):
    start_address = request.GET.get('start')
    end_address = request.GET.get('end')

    if not start_address or not end_address:
        return JsonResponse({
            "status": "error",
            "error": {
                "code": "INVALID_PARAMETERS",
                "message": "Please provide both start and end addresses."
            }
        }, status=400)

    # sanitize inputs
    start_address_sanitized = sanitize_input(start_address)
    end_address_sanitized = sanitize_input(end_address)

    # Construct the cache key using sanitized addresses
    cache_key = f"{start_address_sanitized}_{end_address_sanitized}"
    # cache.delete(cache_key)

    # Check if the result is already cached
    cached_result = cache.get(cache_key)
    if cached_result:
        return JsonResponse(cached_result, status=200)

    # Full-text search for start and end locations
    start_search_query = SearchQuery(start_address_sanitized)
    end_search_query = SearchQuery(end_address_sanitized)
    start_search_vector = SearchVector('name', weight='A') + SearchVector('address', weight='B')
    end_search_vector = SearchVector('name', weight='A') + SearchVector('address', weight='B')

    # Use Trigram Similarity for more nuanced matching
    start_location = Location.objects.annotate(
        rank=SearchRank(start_search_vector, start_search_query),
        similarity=TrigramSimilarity('name', start_address_sanitized) + TrigramSimilarity('address', start_address_sanitized)
    ).filter(similarity__gt=0.3).order_by('-similarity', '-rank').first()

    end_location = Location.objects.annotate(
        rank=SearchRank(end_search_vector, end_search_query),
        similarity=TrigramSimilarity('name', end_address_sanitized) + TrigramSimilarity('address', end_address_sanitized)
    ).filter(similarity__gt=0.3).order_by('-similarity', '-rank').first()

    # Geocode the start and end addresses if not found in the database
    if not start_location:
        start_formatted_address, start_lat, start_lng = LocationService.geocode_address(start_address_sanitized)
        if not start_formatted_address:
            return JsonResponse({
                "status": "error",
                "error": {
                    "code": "GEOCODING_FAILED",
                    "message": "Could not geocode the start address."
                }
            }, status=400)
        start_location = DistanceService.get_or_create_location(
            start_address_sanitized, start_formatted_address, start_lat, start_lng
        )

    if not end_location:
        end_formatted_address, end_lat, end_lng = LocationService.geocode_address(end_address_sanitized)
        if not end_formatted_address:
            return JsonResponse({
                "status": "error",
                "error": {
                    "code": "GEOCODING_FAILED",
                    "message": "Could not geocode the end address."
                }
            }, status=400)
        end_location = DistanceService.get_or_create_location(
            end_address_sanitized, end_formatted_address, end_lat, end_lng
        )

    # Calculate the distance between the start and end locations
    distance_km = LocationService.calculate_distance(start_location.latitude, start_location.longitude, end_location.latitude, end_location.longitude)

    # Check if distance calculation was successful
    if distance_km is None:
        return JsonResponse({
            "status": "error",
            "error": {
                "code": "DISTANCE_CALCULATION_FAILED",
                "message": "Could not calculate distance between the provided locations."
            }
        }, status=400)

    # Save the distance record in the database
    DistanceService.save_distance_record(start_location, end_location, distance_km)

    # Calculate estimated travel time (3 minutes per kilometer)
    estimated_time_minutes = distance_km * 3

    result = {
        "status": "success",
        "data": {
            "start_location": {
                "formatted_address": start_location.address,
                "coordinates": {
                    "latitude": start_location.latitude,
                    "longitude": start_location.longitude
                }
            },
            "end_location": {
                "formatted_address": end_location.address,
                "coordinates": {
                    "latitude": end_location.latitude,
                    "longitude": end_location.longitude
                }
            },
            "route": {
                "distance": {
                    "value": distance_km,
                    "unit": "kilometers"
                },
                "estimated_time": {
                    "value": estimated_time_minutes,
                    "unit": "minutes"
                }
            }
        },
        "metadata": {
            "calculated_at": datetime.utcnow().isoformat() + "Z",
            "service": "Google Maps API"
        }
    }

    # Cache the result with a timeout
    cache.set(cache_key, result, timeout=3600)

    return JsonResponse(result, status=200)
