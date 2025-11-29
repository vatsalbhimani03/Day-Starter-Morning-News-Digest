from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Subscriber:
    email: str
    topics: list[str]
    timezone: str
    send_hour: int = 7
    active: bool = True
    verified: bool = True
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Article:
    title: str
    url: str
    source: str

@dataclass
class DigestResult:
    email: str
    status: str              
    count: int
    created_at: datetime = field(default_factory=datetime.now)