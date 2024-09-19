from datetime import datetime


class DateTimeUtil:
    @classmethod
    def utcnow(cls) -> datetime:
        return datetime.utcnow()

