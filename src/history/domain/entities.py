from dataclasses import dataclass

from datetime import timedelta, date

from task.domain.entities import CategoryEntity
from user.domain.entities import UserEntity


@dataclass
class HistoryEntity:
    id: int
    name: str
    category: CategoryEntity
    user: UserEntity
    planned_time: timedelta
    execution_time: timedelta
    execution_date: date
    status: str


@dataclass
class IncompleteHistoryEntity:
    id: int
    name: str

