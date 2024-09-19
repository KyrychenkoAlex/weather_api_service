import httpx
import logging
import config

from typing import Any

from fastapi import HTTPException

logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self):
        self.appid = config.WEATHER_API_KEY
        self.base_url = config.WEATHER_API_URL

    async def fetch_for_city(self, city: str) -> Any:
        params = dict(
            q=str(city),
            appid=self.appid,
            units='metric'
        )

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, params=params, timeout=10
                )

                response.raise_for_status()

                return response.json()
            except httpx.HTTPError as e:
                status_code = e.response.status_code
                if status_code == 404:
                    raise HTTPException(
                        status_code=404,
                        detail="Resource not found"
                    )
                elif status_code == 500:
                    raise HTTPException(
                        status_code=500,
                        detail="The external API server encountered an error."
                    )
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Internal server error."
                )
