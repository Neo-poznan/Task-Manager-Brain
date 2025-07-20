from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    email: str
    password: str
    last_login: datetime
    is_active: bool
    date_joined: datetime

