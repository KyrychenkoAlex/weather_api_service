import logging

from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse

from schemas.event import EventSchema
from decorators import cache
from services.weather_service import WeatherService
from services.s3_service import S3Service
from services.event_service import EventService
from utils.cache_functions import get_s3_weather_cache_for_city
from utils.datetime_util import DateTimeUtil

weather_router = APIRouter()

logger = logging.getLogger(__name__)


@weather_router.get("/weather/")
@cache(get_s3_weather_cache_for_city)
async def get_weather(
        city: str = Query(..., min_length=1),
        weather_service: WeatherService = Depends(),
        event_service: EventService = Depends(),
        s3: S3Service = Depends()
):
    """
    Endpoint to get weather data for specific city

    :param city:
    :param weather_service:
    :param event_service:
    :param s3:
    :return:
    """
    # fetch from external API
    weather_data = await weather_service.fetch_for_city(city)

    # upload result to S3
    timestamp = int(DateTimeUtil.utcnow().timestamp())
    filename = f"{city}_{timestamp}.json"
    await s3.upload_json(filename, weather_data)

    # save to DynamoDB
    event = EventSchema(
        timestamp=timestamp,
        city=city,
        s3_filename=filename
    )
    await event_service.save_event(event)

    return JSONResponse(content=weather_data)
