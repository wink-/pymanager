# Property Manager

A FastAPI-based property management application for tracking sites, structures, and room details.

## Features

- User authentication with JWT tokens
- Manage multiple sites
- Track structures within sites
- Detailed room information including dimensions and finishes
- RESTful API endpoints for all operations

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database and update .env file with your database credentials:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/property_manager
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit http://localhost:8000/docs for the interactive API documentation.

## Basic Usage

1. Create a user account:
```bash
curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"password123"}'
```

2. Get access token:
```bash
curl -X POST "http://localhost:8000/token" -d "username=user@example.com&password=password123" -H "Content-Type: application/x-www-form-urlencoded"
```

3. Use the token in subsequent requests:
```bash
curl -X GET "http://localhost:8000/sites/" -H "Authorization: Bearer your_access_token"
```
