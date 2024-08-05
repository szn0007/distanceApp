**Distance Calculation API**

This project is a Django-based RESTful API for calculating the distance between two locations using the Google Maps API. It accepts user input for the start and end locations, performs geocoding, and returns the distance along with additional details.

**Features**
1. Geocoding: Converts user-entered addresses into latitude and longitude using Google Maps.
2. Distance Calculation: Computes the distance between two locations.
3. JSON Responses: Provides detailed and structured JSON responses.
4. Error Handling: Includes robust error handling with descriptive messages.

**Prerequisites**
1. Python 3.8 or higher
2. Django 3.2 or higher
3. PostgreSQL (or SQLite for local development)
4. Google Maps API Key

**Installation**
1. Clone the Repository:

```bash
git clone https://github.com/yourusername/distanceapp.git
cd distanceapp
```

2. Create a Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. Install Dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the Database:

Update the DATABASES secrets.json file.

5. Apply Migrations:

```bash
python manage.py migrate
```

6. Set Up Google Maps API Key:

Add your Google Maps API key to the secrets.json file:

```bash
GOOGLE_MAPS_API_KEY = 'your_google_maps_api_key'
```

**Usage**

1. Run the Server:

```bash
python manage.py runserver
```

2. Access the API:

Use the following endpoint to calculate the distance between two locations:

```bash
GET /api/v1/calculate-distance/?start=<start_address>&end=<end_address>
```

Example Request:

```bash
GET /api/v1/calculate-distance/?start=Upper Kharadi Main Rd, Pune&end=HX64+CJW, Pune
```

Example Response:

```bash
{
"status": "success",
"data": {
"start_location": {
"formatted_address": "Upper Kharadi Main Rd, Ubale Nagar, Wagholi, Pune, Maharashtra 412207, India",
"coordinates": {
"latitude": 18.5293,
"longitude": 73.9149
}
},
"end_location": {
"formatted_address": "HX64+CJW, Grant Rd, Ubale Nagar, Kharadi, Pune, Maharashtra 412207, India",
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
"value": 10.824,
"unit": "minutes"
}
}
},
"metadata": {
"calculated_at": "2024-08-04T10:30:00Z",
"service": "Google Maps API"
}
}
```

**Testing**

Run Tests:

To execute the tests for this project, use the following command:

```bash
python manage.py test
```

This command will run the test suite, including tests for successful responses, parameter validation, and error handling.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements or suggestions.
