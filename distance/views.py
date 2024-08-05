from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .services import LocationService, DistanceService

@require_GET
def calculate_distance(request):
    start_address = request.GET.get('start')
    end_address = request.GET.get('end')

    if not start_address or not end_address:
        return JsonResponse({'error': 'Please provide both start and end addresses.'}, status=400)

    start_formatted_address, start_lat, start_lng = LocationService.geocode_address(start_address)
    end_formatted_address, end_lat, end_lng = LocationService.geocode_address(end_address)

    if not start_formatted_address or not end_formatted_address:
        return JsonResponse({'error': 'Could not geocode the provided addresses.'}, status=400)

    start_location = DistanceService.get_or_create_location(start_address, start_formatted_address, start_lat, start_lng)
    end_location = DistanceService.get_or_create_location(end_address, end_formatted_address, end_lat, end_lng)

    distance_km = LocationService.calculate_distance(start_lat, start_lng, end_lat, end_lng)

    if distance_km is None:
        return JsonResponse({'error': 'Could not calculate distance between the provided locations.'}, status=400)

    DistanceService.save_distance_record(start_location, end_location, distance_km)

    return JsonResponse({
        'start_address': start_formatted_address,
        'end_address': end_formatted_address,
        'distance_km': distance_km
    })
