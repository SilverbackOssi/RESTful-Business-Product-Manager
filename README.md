# Product Management API

A RESTful API for managing a business's product catalog with rate limiting to prevent abuse and ensure fair usage.

## Features

- RESTful endpoints for CRUD operations on products
- Rate limiting (100 requests per minute per IP)
- Pagination for large collections
- Professional RESTful responses with proper status codes
- Validation for all required fields
- No authentication required (as per requirements)

## API Documentation

For full API documentation, visit our [GitHub Pages](https://SilverbackOssi.github.io/RESTful-Business-Product-Manager/).

## Tech Stack

- Django 4.2
- Django REST Framework
- Python 3.10+

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository
   ```
   git clone https://github.com/SilverbackOssi/RESTful-Business-Product-Manager.git
   cd product-api
   ```

2. Create a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the development server
   ```
   python manage.py runserver
   ```

6. Access the API at `http://localhost:8000/api/v1/products/`

## Testing with Postman

1. Import the [Postman collection](./postman_collection.json) into Postman
2. Set the `base_url` variable to your API endpoint (default: `http://localhost:8000`)
3. Test each endpoint with the provided examples

## Rate Limiting

All endpoints are rate-limited to 100 requests per minute per IP address. The following headers are included in each response:

- `X-RateLimit-Limit`: The maximum number of requests allowed per time window
- `X-RateLimit-Remaining`: The number of requests remaining in the current time window
- `X-RateLimit-Reset`: Time in seconds until the rate limit is reset

## RESTful Best Practices

This API implements RESTful best practices:
- Proper use of HTTP verbs (GET, POST, PUT, DELETE)
- Resource-based URLs
- API versioning
- Consistent response format
- Appropriate HTTP status codes
- Pagination for collections
- Rate limiting with informative headers

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.