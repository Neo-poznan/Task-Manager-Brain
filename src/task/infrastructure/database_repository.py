from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from django.utils.connection import ConnectionProxy
from django.db.models import Q

from ..models import Category, Task
from user.models import User
from user.domain.entities import UserEntity
from ..domain.entities import TaskEntity, CategoryEntity


class TaskDatabaseRepositoryInterface(ABC):
    @abstractmethod
    def get_ordered_user_tasks(self, user: UserEntity) -> list[TaskEntity]:
        pass


    @abstractmethod
    def get_task_by_id(self, task_id: int) -> TaskEntity:
        pass


    @abstractmethod
    def get_count_user_tasks_in_categories(self, user: UserEntity) -> list[tuple[int, str]]:
        pass


    @abstractmethod
    def get_count_user_tasks_in_categories_by_deadlines(self, user: UserEntity) -> list[tuple[int, str, datetime]]:
        pass

    @abstractmethod
    def save_task(self, task: TaskEntity) -> None:
        pass


class CategoryDatabaseRepositoryInterface(ABC):
    @abstractmethod
    def get_category_by_id(self, category_id: int) -> CategoryEntity:
        pass   


    @abstractmethod
    def get_ordered_user_categories(self, user: UserEntity) -> list[CategoryEntity]:
        pass


class TaskDatabaseRepository(TaskDatabaseRepositoryInterface):
    def __init__(self, model: Task, connection: ConnectionProxy):
        self._model = model
        self._connection = connection

    
    def get_ordered_user_tasks(self, user: UserEntity) -> list[TaskEntity ]:
        return self._model.objects.filter(user=User.from_domain(user)).order_by('order').to_entity_list()


    def get_task_by_id(self, task_id: int) -> TaskEntity:
        return self._model.objects.get(id=task_id).to_domain()
    

    def get_count_user_tasks_in_categories(self, user: UserEntity) -> list[tuple[int, str]]:
        cursor = self._connection.cursor()
        cursor.execute(
            '''
            SELECT count(tt.id), tc.name, tc.color
            FROM task_task tt
            JOIN task_category tc
            ON tt.category_id = tc.id
            WHERE tt.user_id = %s
            GROUP BY tc.name, tc.color
            ORDER BY count(tt.id);
            ''',
            [user.id]
            )
        return cursor.fetchall()
    
    

    def get_count_user_tasks_in_categories_by_deadlines(self, user: UserEntity) -> list[tuple[int, str, datetime]]:
        cursor = self._connection.cursor()
        cursor.execute(
            '''
            SELECT task_deadline, json_agg(json_build_object('count', task_count, 'category', category_name, 'color', color))
            FROM 
            (
                SELECT count(tt.id) AS task_count, tt.deadline AS task_deadline, tc.name AS category_name,  tc.color AS color
                FROM task_task tt join task_category tc on tt.category_id = tc.id 
                WHERE tt.user_id = %s AND tt.deadline IS NOT NULL
                GROUP BY tt.deadline, tc.id, tc.name, tc.color
            )
            GROUP BY task_deadline;
            ''',
            [user.id]
        )
        return cursor.fetchall()
    

    def save_task(self, task: TaskEntity) -> None:
        Task.from_domain(task).save()


class CategoryDatabaseRepository(CategoryDatabaseRepositoryInterface):
    def __init__(self, model: Category):
        self._model = model


    def get_category_by_id(self, category_id: int) -> CategoryEntity:
        return self._model.objects.get(id=category_id).to_domain()
    

    def get_ordered_user_categories(self, user: UserEntity) -> list[CategoryEntity]:
        return self._model.objects.filter(Q(user=User.from_domain(user)) | Q(is_custom=False)).order_by('is_custom').to_entity_list()

