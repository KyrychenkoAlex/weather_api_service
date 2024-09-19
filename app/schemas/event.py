from pydantic import BaseModel


class EventSchema(BaseModel):
    """
    Event schema
    """
    timestamp: int
    s3_filename: str
    city: str
