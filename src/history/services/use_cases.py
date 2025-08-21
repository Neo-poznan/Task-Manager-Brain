from abc import ABC, abstractmethod
from decimal import Decimal

from user.domain.entities import UserEntity
from ..infrastructure.database_repository import HistoryDatabaseRepositoryInterface
from task.serializers import to_json


class HistoryUseCaseInterface(ABC):
    @abstractmethod
    def get_user_history_statistics(self, user: UserEntity):
        pass


class HistoryUseCase(HistoryUseCaseInterface):
    def __init__(self, history_database_repository: HistoryDatabaseRepositoryInterface):
        self._history_database_repository = history_database_repository
    

    def get_user_history_statistics(self, user: UserEntity):
        raw_count_user_tasks_in_categories = self._history_database_repository.get_count_user_tasks_in_categories(user)
        raw_common_user_accuracy = self._history_database_repository.get_common_user_accuracy(user)
        raw_user_accuracy_by_categories = self._history_database_repository.get_user_accuracy_by_categories(user)
        raw_common_user_success_rate = self._history_database_repository.get_user_common_success_rate(user)
        raw_user_success_rate_by_categories = self._history_database_repository.get_user_success_rate_by_categories(user)
        raw_count_user_tasks_by_weekdays = self._history_database_repository.get_count_user_tasks_by_weekdays(user)   
        raw_common_count_successful_planned_tasks = self._history_database_repository.get_common_count_user_successful_planned_tasks(user)
        raw_count_successful_planned_tasks_by_categories = self._history_database_repository.get_count_user_successful_planned_tasks_by_categories(user)

        return {
            'count_user_tasks_in_categories': to_json(self._format_count_user_tasks_in_categories(raw_count_user_tasks_in_categories)),
            'common_user_accuracy': to_json(self._format_common_user_accuracy(raw_common_user_accuracy)),
            'user_accuracy_by_categories': to_json(self._format_user_accuracy_by_categories(raw_user_accuracy_by_categories)),
            'common_user_success_rate': to_json(self._format_common_user_success_rate(raw_common_user_success_rate)),
            'user_success_rate_by_categories': to_json(self._format_user_success_rate_by_categories(raw_user_success_rate_by_categories)),
            'count_user_tasks_by_weekdays': to_json(self._format_count_user_tasks_by_weekdays(raw_count_user_tasks_by_weekdays)),
            'common_count_user_successful_planned_tasks': to_json(self._format_common_count_user_successful_planned_tasks(raw_common_count_successful_planned_tasks)),
            'count_user_successful_planned_tasks_by_categories': to_json(self._format_count_user_successful_planned_tasks_by_categories(raw_count_successful_planned_tasks_by_categories))
        }

 
    def _format_count_user_tasks_in_categories(self, raw_count_user_tasks_in_categories: list[tuple[str, int]]) -> dict[str, list]:
        count_user_tasks_in_categories = {'labels': [], 'colors': [], 'data': []}
        for row in raw_count_user_tasks_in_categories:
            count_user_tasks_in_categories['labels'].append(row[0])
            count_user_tasks_in_categories['colors'].append(row[1])
            count_user_tasks_in_categories['data'].append(row[2])
        return count_user_tasks_in_categories
    
    def _format_common_user_accuracy(self, raw_common_user_accuracy: list[tuple[Decimal]]) -> dict[str, list]:
        return {
                'labels': ['Точность', 'Точность'],
                'colors': ['rgba(0, 255, 0, 0.4)', 'rgba(255, 0, 0, 0.4)'],
                'data': [float(raw_common_user_accuracy[0][0]), 100.0 - float(raw_common_user_accuracy[0][0])]
            }
    
    def _format_user_accuracy_by_categories(self, raw_user_accuracy_by_categories: list[tuple[str, Decimal]]) -> dict[str, list]:
        user_accuracy_by_categories = {'labels': [], 'colors': [], 'data': []}
        for row in raw_user_accuracy_by_categories:
            user_accuracy_by_categories['labels'].append(row[0])
            user_accuracy_by_categories['colors'].append(row[1])
            user_accuracy_by_categories['data'].append(float(row[2]))
        return user_accuracy_by_categories
    
    def _format_common_user_success_rate(self, raw_common_user_success_rate: list[tuple[int]]) -> dict[str, list]:
        return {
            'labels': ['Выполненные задачи', 'Проваленные задачи'],
            'colors': ['rgba(0, 255, 0, 0.4)', 'rgba(255, 0, 0, 0.4)'],
            'data': [float(raw_common_user_success_rate[0][0]), float(raw_common_user_success_rate[0][1])]
        }
    
    def _format_user_success_rate_by_categories(self, raw_user_success_rate_by_categories: list[tuple[str, int]]) -> dict[str, list]:
        user_success_rate_by_categories = {'labels': [], 'colors': [], 'data': []}
        for row in raw_user_success_rate_by_categories:
            user_success_rate_by_categories['labels'].append(row[0])
            user_success_rate_by_categories['colors'].append(row[1])
            user_success_rate_by_categories['data'].append(row[2]) 
        return user_success_rate_by_categories
    
    def _format_count_user_tasks_by_weekdays(self, raw_count_user_tasks_by_weekdays: list[tuple[str, int]]) -> dict[str, list]:
        count_user_tasks_by_weekdays = {'labels': [], 'data': []}
        for row in raw_count_user_tasks_by_weekdays:
            count_user_tasks_by_weekdays['labels'].append(row[0])
            count_user_tasks_by_weekdays['data'].append(row[1]) 
        return count_user_tasks_by_weekdays
    
    def _format_common_count_user_successful_planned_tasks(self, raw_common_count_successful_planned_tasks: list[tuple[int]]) -> dict[str, list]:
        return {
            'labels': ['Успешно запланированные задачи', 'Неправильно запланированные задачи'],
            'colors': ['rgba(0, 255, 0, 0.4)', 'rgba(255, 0, 0, 0.4)'],
            'data': [raw_common_count_successful_planned_tasks[0][0], raw_common_count_successful_planned_tasks[0][1]]
        } 

    def _format_count_user_successful_planned_tasks_by_categories(self, raw_count_successful_planned_tasks_by_categories: list[tuple[str, int]]) -> dict[str, list]:
        count_successful_planned_tasks_by_categories = {'labels': [], 'colors': [], 'data': []}
        for row in raw_count_successful_planned_tasks_by_categories:
            count_successful_planned_tasks_by_categories['labels'].append(row[0])
            count_successful_planned_tasks_by_categories['colors'].append(row[1])
            count_successful_planned_tasks_by_categories['data'].append(row[2]) 
        return count_successful_planned_tasks_by_categories

