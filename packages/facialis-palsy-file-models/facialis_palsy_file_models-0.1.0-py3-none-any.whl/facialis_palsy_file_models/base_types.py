from datetime import datetime
from typing import Any

from pydantic import BaseModel, validator


class KeyValue(BaseModel):
    """
    Key Value Pair with automatic timestamp
    """

    key: str
    value: Any
    time: str = None

    # Time imPort ggf mit strptime
    # QDateTime(datetime.datetime.strptime(f"{k.time}", "%Y-%m-%d %H:%M:%S.%f"))

    def __init__(self, **data) -> None:
        super(KeyValue, self).__init__(**data)
        if self.time is None:
            self.time = f"{datetime.now()}"

