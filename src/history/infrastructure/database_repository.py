from abc import ABC, abstractmethod
from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.utils.connection import ConnectionProxy

from ..models import History
from task.models import Task
from task.domain.entities import TaskEntity
from user.domain.entities import UserEntity


class HistoryDatabaseRepositoryInterface(ABC):
    @abstractmethod
    def save_task_to_history_as_successful(self, task: TaskEntity, execution_time: timedelta) -> None:
        pass


    @abstractmethod
    def save_task_to_history_as_outed_of_deadline(self, task: TaskEntity, execution_time: timedelta) -> None:
        pass


    @abstractmethod
    def save_task_to_history_as_failed(self, task: TaskEntity, execution_time: timedelta) -> None:
        pass


    @abstractmethod
    def get_count_user_tasks_in_categories(self, user: UserEntity) -> list[tuple[int, str]]:
        pass


    @abstractmethod
    def get_common_user_accuracy(self, user: UserEntity) -> list[tuple[Decimal]]:
        pass


    @abstractmethod
    def get_user_accuracy_by_categories(self, user: UserEntity) -> list[tuple[str, Decimal]]:
        pass


    @abstractmethod
    def get_user_common_success_rate(self, user: UserEntity) -> list[tuple[Decimal]]:
        pass


    @abstractmethod
    def get_user_success_rate_by_categories(self, user: UserEntity) -> list[tuple[str, Decimal]]:
        pass


    @abstractmethod
    def get_count_user_tasks_by_weekdays(self, user: UserEntity) -> list[tuple[str, int]]:
        pass


    @abstractmethod
    def get_common_count_user_successful_planned_tasks(self, user: UserEntity) -> list[tuple[int]]:
        pass


    @abstractmethod
    def get_count_user_successful_planned_tasks_by_categories(self, user: UserEntity) -> list[tuple[str, int]]:
        pass


class HistoryDatabaseRepository(HistoryDatabaseRepositoryInterface):
    def __init__(self, task_model: Task, history_model: History, connection: ConnectionProxy):
        self._task_model = task_model
        self._history_model = history_model
        self._connection = connection

    
    @transaction.atomic
    def save_task_to_history_as_successful(self, task: TaskEntity, execution_time: timedelta) -> None:
        task_model_obj = self._task_model.from_domain(task)
        task_model_obj.delete()
        self._history_model.objects.create(
                name=task_model_obj.name,
                category=task_model_obj.category,
                user=task_model_obj.user,
                planned_time=task_model_obj.planned_time,
                execution_time=execution_time,
                status=self._history_model.SUCCESSFUL
            )

    
    @transaction.atomic
    def save_task_to_history_as_outed_of_deadline(self, task: TaskEntity, execution_time: timedelta) -> None:
        task_model_obj = self._task_model.from_domain(task)
        task_model_obj.delete()
        self._history_model.objects.create(
                name=task_model_obj.name,
                category=task_model_obj.category,
                user=task_model_obj.user,
                planned_time=task_model_obj.planned_time,
                execution_time=execution_time,
                status=self._history_model.OUT_OF_DEADLINE
            )
        
    
    @transaction.atomic
    def save_task_to_history_as_failed(self, task: TaskEntity, execution_time: timedelta) -> None:
        task_model_obj = self._task_model.from_domain(task)
        task_model_obj.delete()
        self._history_model.objects.create(
                name=task_model_obj.name,
                category=task_model_obj.category,
                user=task_model_obj.user,
                planned_time=task_model_obj.planned_time,
                execution_time=execution_time,
                status=self._history_model.FAILED
            )
        
    
    def get_count_user_tasks_in_categories(self, user: UserEntity) -> list[tuple[int, str]]:
        cursor = self._connection.cursor()
        cursor.execute(
            '''
            SELECT tc.name, tc.color, count(hh.id)
            FROM history_history hh
            JOIN task_category tc
            ON hh.category_id = tc.id
            WHERE hh.user_id = %s
            GROUP BY tc.name, tc.color
            ORDER BY count(hh.id);
            ''',
            [user.id]
        )
        return cursor.fetchall()

    
    def get_common_user_accuracy(self, user: UserEntity) -> list[tuple[Decimal]]:
        cursor = self._connection.cursor()
        cursor.execute(
            '''
            SELECT
            round(avg(
            CASE 
                WHEN extract(epoch FROM planned_time) = 0 or extract(epoch FROM execution_time) = 0 THEN 0
                WHEN planned_time < execution_time THEN (extract(epoch FROM planned_time) / extract(epoch FROM execution_time)) * 100
                WHEN planned_time > execution_time THEN (extract(epoch FROM execution_time) / extract(epoch FROM planned_time)) * 100
            END), 2) AS accuracy
            FROM history_history
            WHERE user_id = %s;
            ''',
            [user.id]
        )
        return cursor.fetchall()


    def get_user_accuracy_by_categories(self, user: UserEntity) -> list[tuple[str, Decimal]]:
        cursor = self._connection.cursor()
        cursor.execute(
            '''
            SELECT
            tc.name, tc.color,
            round(avg(
            CASE 
                WHEN extract(epoch FROM planned_time) = 0 OR extract(epoch FROM execution_time) = 0 THEN NULL
                WHEN planned_time < execution_time THEN (extract(epoch FROM planned_time) / extract(epoch FROM execution_time)) * 100
                WHEN planned_time > execution_time THEN (extract(epoch FROM execution_time) / extract(epoch FROM planned_time)) * 100
            END), 2) AS accuracy
            FROM history_history hh
            JOIN task_category tc
            ON hh.category_id = tc.id
            WHERE hh.user_id = %s
            GROUP BY category_id, tc."name", tc.color
            ORDER BY accuracy;
            ''',
            [user.id]
        )
        return cursor.fetchall()


    def get_user_common_success_rate(self, user: UserEntity) -> list[tuple[Decimal]]:
        cursor = self._connection.cursor()
        cursor.execute(
            '''
            SELECT count(*)-(SELECT count(*) FROM history_history hh2 WHERE hh2.status='FAILED' AND hh2.user_id = %s) AS successful_tasks,
            (SELECT count(*) FROM history_history hh3 WHERE hh3.status='FAILED' AND hh3.user_id = %s) AS failed_tasks 
            FROM history_history hh
            WHERE hh.user_id = %s;
            ''',
            [user.id, user.id, user.id]
        )
        return cursor.fetchall()


    def get_user_success_rate_by_categories(self, user: UserEntity) -> list[tuple[str, float]]:
        cursor = self._connection.cursor()
        cursor.execute(
            '''
            SELECT
            tc."name", tc.color,
            count(*)-(SELECT count(*) FROM history_history hh2 WHERE hh2.status='FAILED' AND hh2.category_id=hh.category_id AND hh2.user_id = %s) AS successful_tasks
            FROM history_history hh 
            join task_category tc 
            ON hh.category_id = tc.id
            WHERE hh.user_id = %s
            GROUP BY category_id, tc."name", tc.color;
            ''',
            [user.id, user.id]
        )
        return cursor.fetchall()


    def get_count_user_tasks_by_weekdays(self, user: UserEntity) -> list[tuple[str, int]]:
        cursor = self._connection.cursor()
        cursor.execute(
            '''
            SELECT day_name, count(hh.id) AS task_count FROM (VALUES
                (1, 'Понедельник'),
                (2, 'Вторник'),
                (3, 'Среда'),
                (4, 'Четверг'),
                (5, 'Пятница'),
                (6, 'Суббота'),
                (7, 'Воскресенье')
            ) weekdays(day_index, day_name)
            LEFT join history_history hh ON day_index=extract(isodow FROM hh.execution_date)
            WHERE hh.user_id = %s
            GROUP BY day_index, day_name
            ORDER BY day_index;
            ''',
            [user.id]
        )
        return cursor.fetchall()


    def get_common_count_user_successful_planned_tasks(self, user: UserEntity) -> list[tuple[int]]:
        cursor = self._connection.cursor()
        cursor.execute(
            '''
            SELECT
            (SELECT count(hh2.id) FROM history_history hh2 WHERE hh2.user_id = %s AND hh2.planned_time = hh2.execution_time) AS successful_planning,
            count(hh.id) AS failed_planning
            FROM history_history hh 
            WHERE hh.user_id = %s AND hh.planned_time != hh.execution_time; 
            ''',
            [user.id, user.id]
        )
        return cursor.fetchall()

    
    def get_count_user_successful_planned_tasks_by_categories(self, user: UserEntity) -> list[tuple[str, int]]:
        cursor = self._connection.cursor()
        cursor.execute(
            '''
            SELECT
            tc."name",
            tc.color,
            count(hh.id) AS successful_planning
            from history_history hh 
            JOIN task_category tc 
            ON tc.id = hh.category_id 
            WHERE hh.user_id = %s AND hh.planned_time = hh.execution_time
            GROUP BY hh.category_id, tc."name", tc.color;
            ''',
            [user.id]
        )
        return cursor.fetchall()

