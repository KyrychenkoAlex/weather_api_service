from fastapi import FastAPI, APIRouter

from routers.weather_router import weather_router
from utils.create_table import create_table

app = FastAPI()
router = APIRouter()

app.include_router(weather_router)


@app.on_event("startup")
def startup_event():
    create_table(
        'events_table',
        [
            {
                'AttributeName': 'timestamp',
                'KeyType': 'HASH'
            },
        ],
        [
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'N'
            },
        ]
    )
