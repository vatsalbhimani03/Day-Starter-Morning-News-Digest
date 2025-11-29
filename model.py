from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class Subscriber:
    email: str
    topics: List[str]
    timezone: str
    send_hour: int = 7
    active: bool = True
    verified: bool = True
    created_at: datetime = field(default_factory=datetime.now)