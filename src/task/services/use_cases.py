from abc import ABC, abstractmethod
from datetime import timedelta

from ..infrastructure.database_repository import TaskDatabaseRepositoryInterface, CategoryDatabaseRepositoryInterface
from user.domain.entities import UserEntity
from ..domain.entities import TaskEntity, CategoryEntity
from ..helpers.colors import generate_random_hex_color, hex_color_to_rgba_with_default_obscurity, rgba_color_with_default_obscurity_to_hex
from ..helpers.date import is_out_of_deadline
from history.infrastructure.database_repository import HistoryDatabaseRepositoryInterface


class TaskUseCaseInterface(ABC):
    @abstractmethod
    def get_next_task_order(self, user: UserEntity):
        pass


    @abstractmethod
    def get_random_hex_color(self) -> str:
        pass


    @abstractmethod
    def get_rgba_color_with_default_obscurity(self, hex_color: str) -> str:
        pass


    @abstractmethod
    def get_user_task_by_id(self, task_id: int, user: UserEntity) -> TaskEntity:
        pass


    @abstractmethod
    def get_user_category_by_id(self, category_id: int, user: UserEntity) -> CategoryEntity:
        pass


    @abstractmethod
    def get_hex_color_by_category_id(self, category_id: int) -> str:
        pass


    @abstractmethod
    def get_user_task_count_statistics(self, user: UserEntity) -> dict[str, list]:
        pass


    @abstractmethod
    def get_user_task_deadlines_count_statistics(self, user: UserEntity) -> dict[str, list]:
        pass


    @abstractmethod
    def update_user_task_order(self, user: UserEntity, new_order: list[str]):
        pass


    @abstractmethod
    def get_ordered_user_tasks(self, user: UserEntity) -> list[TaskEntity]:
        pass


    @abstractmethod
    def get_ordered_user_categories(self, user: UserEntity) -> list[CategoryEntity]:
        pass


    @abstractmethod
    def update_user_task_order(self, user: UserEntity, new_order: list[str]) -> None:
        pass


    @abstractmethod
    def save_completed_task_to_history(self, user: UserEntity, task_id: int, execution_time: timedelta) -> None:
        pass


    @abstractmethod
    def save_failed_task_to_history(self, user: UserEntity, task_id: int, execution_time: timedelta) -> None:
        pass


class TaskUseCase(TaskUseCaseInterface):
    def __init__(
                self, task_database_repository: TaskDatabaseRepositoryInterface = None,
                category_database_repository: CategoryDatabaseRepositoryInterface = None,
                history_database_repository: HistoryDatabaseRepositoryInterface = None
            ):
        self._task_database_repository = task_database_repository
        self._category_database_repository = category_database_repository
        self._history_database_repository = history_database_repository

    
    def get_next_task_order(self, user: UserEntity) -> int:
        user_tasks = self._task_database_repository.get_ordered_user_tasks(user)
        if user_tasks:
            return user_tasks[-1].order + 1
        else:
            return 1
    

    def get_random_hex_color(self) -> str:
        return generate_random_hex_color()

    
    def get_rgba_color_with_default_obscurity(self, hex_color: str) -> str:
        return hex_color_to_rgba_with_default_obscurity(hex_color)


    def get_user_task_by_id(self, task_id: int, user: UserEntity) -> TaskEntity:
        task = self._task_database_repository.get_task_by_id(task_id)
        if task.user == user:
            return task
        else:
            raise PermissionError

    
    def get_user_category_by_id(self, category_id: int, user: UserEntity) -> CategoryEntity:
        category = self._category_database_repository.get_category_by_id(category_id)
        # Это исключение будет райзиться не только тогда, когда пользователь пытается редактировать чужую задачу, но и тогда, 
        # когда категория не является кастомной, и, соответственно не имеет пользователя
        if category.user != user:
            raise PermissionError 
        return category


    def get_hex_color_by_category_id(self, category_id: int) -> str:
        rgba_color = self._category_database_repository.get_category_by_id(category_id).color   
        return rgba_color_with_default_obscurity_to_hex(rgba_color)
    

    def get_user_task_count_statistics(self, user: UserEntity) -> dict[str, list]:
        raw__task_count_statistics = self._task_database_repository.get_count_user_tasks_in_categories(user)
        task_counts = []
        category_names = []
        category_colors = []
        for row in raw__task_count_statistics:
            task_counts.append(row[0])
            category_names.append(row[1])
            category_colors.append(row[2])
        return {'counts': task_counts, 'categories': category_names, 'colors': category_colors}
    

    def get_user_task_deadlines_count_statistics(self, user: UserEntity) -> dict[str, list]:
        raw_task_deadlines_count_statistics = self._task_database_repository.get_count_user_tasks_in_categories_by_deadlines(user)
        deadlines_count_statistics = {}
        for row in raw_task_deadlines_count_statistics:
            deadlines_count_statistics[row[0].strftime('%Y.%m.%d')] = row[1]
        print(deadlines_count_statistics)
        return deadlines_count_statistics
    

    def get_ordered_user_tasks(self, user: UserEntity) -> list[TaskEntity]:
        return self._task_database_repository.get_ordered_user_tasks(user)
    

    def get_ordered_user_categories(self, user: UserEntity) -> list[CategoryEntity]:
        return self._category_database_repository.get_ordered_user_categories(user)
    

    def update_user_task_order(self, user: UserEntity, new_order: list[str]) -> None:
        user_tasks = self._task_database_repository.get_ordered_user_tasks(user)
        task_dict = {task.id: task for task in user_tasks}
        for list_index, task_id in enumerate(new_order):
            if task_dict[int(task_id)].order != list_index + 1:
                updated_task = task_dict[int(task_id)]
                updated_task.order = list_index + 1
                self._task_database_repository.save_task(updated_task)


    def save_completed_task_to_history(self, user: UserEntity, task_id: int, execution_time: timedelta) -> None:
        task = self._task_database_repository.get_task_by_id(task_id)
        if task.user != user:
            raise PermissionError
        if not is_out_of_deadline(task.deadline):
            self._history_database_repository.save_task_to_history_as_successful(task, execution_time)
        else:
            self._history_database_repository.save_task_to_history_as_outed_of_deadline(task, execution_time)


    def save_failed_task_to_history(self, user: UserEntity, task_id: int, execution_time: timedelta) -> None:
        task = self._task_database_repository.get_task_by_id(task_id)
        if task.user != user:
            raise PermissionError
        self._history_database_repository.save_task_to_history_as_failed(task, execution_time)

