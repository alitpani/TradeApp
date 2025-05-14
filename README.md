# Stock Trades API

A Django REST API for managing stock trades with JWT authentication.

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv (recommended)
- Docker and Docker Compose
- PostgreSQL (if not using Docker)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/alitpani/TradeApp.git
cd stocktrades
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start PostgreSQL using Docker:
```bash
docker-compose up -d
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser (admin):
```bash
python manage.py createsuperuser
# Follow the prompts to create username, email, and password
```

7. Run the development server:
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

## Testing

### Unit Tests
Run the test suite using:
```bash
python manage.py test
```

### Load Testing with Locust
The project includes Locust for load testing. To run the load tests:

1. Start the Django server
2. In a separate terminal, run:
```bash
locust -f locustfile.py
```
3. Open http://localhost:8089 in your browser
4. Configure the number of users and spawn rate
5. Start the test

The Locust dashboard will show real-time metrics about the API's performance under load.

## API Documentation

The API is documented in Postman. You can access the complete API documentation and test the endpoints using the following Postman collection:

[Stock Trades API Collection](https://www.postman.com/bold-resonance-867817/workspace/fundsindia/collection/6250266-10e0e0bd-3496-48a7-a097-7ae3556d4efa?action=share&source=copy-link&creator=6250266&active-environment=0aededff-0e8a-43aa-804b-ef4b62193ead)

### Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. Get access token:
```bash
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

2. Refresh token:
```bash
POST /api/token/refresh/
{
    "refresh": "your_refresh_token"
}
```

### Available Endpoints

- `POST /api/trades/` - Create a new trade
- `GET /api/trades/` - List all trades (with optional filters)
- `GET /api/trades/<id>/` - Get specific trade
- `PUT/PATCH/DELETE /api/trades/<id>/` - Not allowed (returns 405)

### Trade Object Structure

```json
{
    "id": 1,
    "type": "buy",
    "user_id": 23,
    "symbol": "ABX",
    "shares": 30,
    "price": 134,
    "timestamp": 1531522701000
}
```

### Validation Rules

- `type` must be either "buy" or "sell"
- `shares` must be between 1 and 100
- All fields except `id` and `timestamp` are required
- `timestamp` is automatically generated

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@localhost:5432/stocktrades
```

## Docker Configuration

The project uses Docker Compose to run PostgreSQL. The configuration is in `docker-compose.yml`:

```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: stocktrades
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

To manage the Docker container:
- Start: `docker-compose up -d`
- Stop: `docker-compose down`
- View logs: `docker-compose logs -f`
- Remove volumes: `docker-compose down -v`
