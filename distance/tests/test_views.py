from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from datetime import datetime

class DistanceViewTest(TestCase):

    def setUp(self):
        # Initialize the test client
        self.client = Client()

    @patch('distance.services.LocationService.geocode_address')
    @patch('distance.services.LocationService.calculate_distance')
    def test_calculate_distance_view_success(self, mock_calculate_distance, mock_geocode_address):
        # Mock the responses for geocode and distance calculation
        mock_geocode_address.side_effect = [
            ("Start Address", 18.5293, 73.9149),  # Start location
            ("End Address", 18.5523, 73.9340)     # End location
        ]
        mock_calculate_distance.return_value = 3.608  # Mocked distance in kilometers

        # Perform a GET request to the calculate_distance endpoint
        response = self.client.get(reverse('calculate_distance'), {
            'start': 'Start Location',
            'end': 'End Location'
        })

        # Define the expected JSON response structure
        expected_response = {
            "status": "success",
            "data": {
                "start_location": {
                    "formatted_address": "Start Address",
                    "coordinates": {
                        "latitude": 18.5293,
                        "longitude": 73.9149
                    }
                },
                "end_location": {
                    "formatted_address": "End Address",
                    "coordinates": {
                        "latitude": 18.5523,
                        "longitude": 73.9340
                    }
                },
                "route": {
                    "distance": {
                        "value": 3.608,
                        "unit": "kilometers"
                    },
                    "estimated_time": {
                        "value": 10.824,  # Assuming 3 minutes per kilometer
                        "unit": "minutes"
                    }
                }
            },
            "metadata": {
                "calculated_at": datetime.utcnow().isoformat()[:-7] + "Z",
                "service": "Google Maps API"
            }
        }

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Compare the actual JSON response to the expected response structure
        actual_response = response.json()
        
        # Adjust the comparison for metadata as time may vary slightly
        self.assertEqual(actual_response['status'], expected_response['status'])
        self.assertEqual(actual_response['data'], expected_response['data'])
        self.assertEqual(actual_response['metadata']['service'], expected_response['metadata']['service'])

    def test_calculate_distance_view_missing_parameters(self):
        # Test for missing 'start' parameter
        response = self.client.get(reverse('calculate_distance'), {'end': 'End Location'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "status": "error",
            "error": {
                "code": "INVALID_PARAMETERS",
                "message": "Please provide both start and end addresses."
            }
        })

        # Test for missing 'end' parameter
        response = self.client.get(reverse('calculate_distance'), {'start': 'Start Location'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "status": "error",
            "error": {
                "code": "INVALID_PARAMETERS",
                "message": "Please provide both start and end addresses."
            }
        })

        # Test for missing both parameters
        response = self.client.get(reverse('calculate_distance'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "status": "error",
            "error": {
                "code": "INVALID_PARAMETERS",
                "message": "Please provide both start and end addresses."
            }
        })

    @patch('distance.services.LocationService.geocode_address')
    def test_calculate_distance_view_geocoding_failure(self, mock_geocode_address):
        # Mock geocoding to return None indicating failure
        mock_geocode_address.return_value = (None, None, None)

        response = self.client.get(reverse('calculate_distance'), {
            'start': 'Start Location',
            'end': 'End Location'
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "status": "error",
            "error": {
                "code": "GEOCODING_FAILED",
                "message": "Could not geocode the start address."
            }
        })

    @patch('distance.services.LocationService.geocode_address')
    @patch('distance.services.LocationService.calculate_distance')
    def test_calculate_distance_view_distance_calculation_failure(self, mock_calculate_distance, mock_geocode_address):
        # Mock successful geocoding
        mock_geocode_address.side_effect = [
            ("Start Address", 18.5293, 73.9149),  # Start location
            ("End Address", 18.5523, 73.9340)     # End location
        ]
        
        # Mock distance calculation to return None indicating failure
        mock_calculate_distance.return_value = None

        response = self.client.get(reverse('calculate_distance'), {
            'start': 'Start Location',
            'end': 'End Location'
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "status": "error",
            "error": {
                "code": "DISTANCE_CALCULATION_FAILED",
                "message": "Could not calculate distance between the provided locations."
            }
        })

    @patch('distance.services.LocationService.geocode_address')
    @patch('distance.services.LocationService.calculate_distance')
    def test_calculate_distance_view_with_similar_names(self, mock_calculate_distance, mock_geocode_address):
        # Mock the responses for geocode and distance calculation
        mock_geocode_address.side_effect = [
            ("Walt Disney Concert Hall", 34.055, -118.249),  # Start location
            ("Disney Concert Hall", 34.055, -118.249)       # End location
        ]
        mock_calculate_distance.return_value = 0.0  # Same location, so distance is 0

        response = self.client.get(reverse('calculate_distance'), {
            'start': 'Walt Disney Concert Hall',
            'end': 'Disney Concert Hall'
        })

        expected_response = {
            "status": "success",
            "data": {
                "start_location": {
                    "formatted_address": "Walt Disney Concert Hall",
                    "coordinates": {
                        "latitude": 34.055,
                        "longitude": -118.249
                    }
                },
                "end_location": {
                    "formatted_address": "Disney Concert Hall",
                    "coordinates": {
                        "latitude": 34.055,
                        "longitude": -118.249
                    }
                },
                "route": {
                    "distance": {
                        "value": 0.0,
                        "unit": "kilometers"
                    },
                    "estimated_time": {
                        "value": 0.0,
                        "unit": "minutes"
                    }
                }
            },
            "metadata": {
                "calculated_at": datetime.utcnow().isoformat()[:-7] + "Z",
                "service": "Google Maps API"
            }
        }

        self.assertEqual(response.status_code, 200)
        actual_response = response.json()
        self.assertEqual(actual_response['status'], expected_response['status'])
        self.assertEqual(actual_response['data'], expected_response['data'])
        self.assertEqual(actual_response['metadata']['service'], expected_response['metadata']['service'])

