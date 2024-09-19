# Weather API Service

## Description

A FastAPI-based service that provides current weather data for a specified city. 
It fetches data from the OpenWeatherMap API, caches responses to minimize redundant 
external calls, and logs each request to a database.

## Technologies Used

- **FastAPI**
- **Python 3.11**
- **httpx**
- **aioboto3**
- **MinIO** (S3 equivalent)
- **DynamoDB Local** (DynamoDB equivalent)
- **Docker & Docker Compose**
- **Uvicorn**

## Prerequisites

- **Docker** and **Docker Compose** installed.
- **Git** installed.
- An **OpenWeatherMap API Key**.

## Installation & Setup

1. **Clone the Repository**
2. Copy `.env.example` to `.env`
3. Add your `WEATHER_API_KEY`
4. Run: `docker-compose -f docker/docker-compose.yml up -d --build`
5. Go to the `http://localhost:9001/`
6. Create bucked and add this name to the env file as `S3_BUCKET_NAME` variable
7. Re-run docker 
8. Done