import os

# External Weather API Configuration
WEATHER_API_URL = os.getenv("WEATHER_API_URL")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# AWS S3 Configuration
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "weather-data")
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'http://localhost:9000')

# AWS DynamoDB Configuration
DYNAMODB_ENDPOINT_URL = os.getenv('DYNAMODB_ENDPOINT_URL',
                                  'http://localhost:8000')

# AWS keys
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

# Caching Configuration
CACHE_EXPIRY_MINUTES = 5
