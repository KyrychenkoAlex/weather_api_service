from fastapi import Depends

from schemas.event import EventSchema
from repositories.event import EventRepository


class EventService:
    event_repository: EventRepository

    def __init__(
            self,
            event_repository: EventRepository = Depends(),
    ) -> None:
        self.event_repository = event_repository

    async def save_event(self, data: EventSchema):
        await self.event_repository.create(data)
