from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .services import LocationService, DistanceService
from datetime import datetime

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

    start_formatted_address, start_lat, start_lng = LocationService.geocode_address(start_address)
    end_formatted_address, end_lat, end_lng = LocationService.geocode_address(end_address)

    if not start_formatted_address or not end_formatted_address:
        return JsonResponse({
            "status": "error",
            "error": {
                "code": "GEOCODING_FAILED",
                "message": "Could not geocode the provided addresses."
            }
        }, status=400)

    start_location = DistanceService.get_or_create_location(
        start_address, start_formatted_address, start_lat, start_lng
    )
    end_location = DistanceService.get_or_create_location(
        end_address, end_formatted_address, end_lat, end_lng
    )

    # Calculate the distance
    distance_km = LocationService.calculate_distance(start_lat, start_lng, end_lat, end_lng)

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

    return JsonResponse({
        "status": "success",
        "data": {
            "start_location": {
                "formatted_address": start_formatted_address,
                "coordinates": {
                    "latitude": start_lat,
                    "longitude": start_lng
                }
            },
            "end_location": {
                "formatted_address": end_formatted_address,
                "coordinates": {
                    "latitude": end_lat,
                    "longitude": end_lng
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
    }, status=200)
