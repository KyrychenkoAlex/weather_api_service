import functools
import logging

from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def cache(get_cache_function):
    """
    Decorator to cache data
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cached_data = await get_cache_function(*args, **kwargs)
            if cached_data:
                return JSONResponse(content=cached_data)

            response = await func(*args, **kwargs)
            return response

        return wrapper

    return decorator