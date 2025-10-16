import json
from django.db import models
from django.contrib.auth import get_user_model

from task.models import Category, DomainQuerySet
from user.models import User
from .domain.entities import HistoryEntity, SharedHistoryEntity


class History(models.Model):
    SUCCESSFUL = 'SUCCESSFUL'
    OUT_OF_DEADLINE = 'OUT_OF_DEADLINE'
    FAILED = 'FAILED'

    STATUS_CHOICES = (
        (SUCCESSFUL, 'Успешно выполнена вовремя'),
        (OUT_OF_DEADLINE, 'Выполнена с опозданием'),
        (FAILED, 'Провалена'),
    )

    name = models.CharField(max_length=290, null=False, blank=False, verbose_name='Название задачи')
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория задачи')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, null=False, blank=False, verbose_name='Пользователь, создавший задачу')
    planned_time = models.DurationField(null=False, blank=False, verbose_name='Время, которое было изначально запланировано на процесс выполнения задачи')
    execution_time = models.DurationField(null=False, blank=False, verbose_name='Время, которое реально потребовалось на выполнение задачи')
    execution_date = models.DateField(null=False, blank=False, auto_now_add=True, verbose_name='День, в который была выполнена задача')
    status = models.CharField(max_length=50, null=False, blank=False, choices=STATUS_CHOICES, verbose_name='Статус, к примеру, была задача выполнена или провалена')

    objects = DomainQuerySet.as_manager()

    @classmethod
    def from_domain(cls, entity: HistoryEntity):
        return cls(
            id=entity.id,
            name=entity.name,
            user=User.from_domain(entity.user),
            category=Category.from_domain(entity.category),
            planned_time=entity.planned_time,
            execution_time=entity.execution_time,
            execution_date=entity.execution_date,
            status=entity.status
        )

    def to_domain(self) -> HistoryEntity:
        return HistoryEntity(
            id=self.id,
            name=self.name,
            user=self.user.to_domain(),
            category=self.category.to_domain(),
            planned_time=self.planned_time,
            execution_time=self.execution_time,
            execution_date=self.execution_date,
            status=self.status
        )


    class Meta:
        verbose_name = 'История выполненных и проваленных задач. Одна строка - одна задача.'


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj.__iter__:
            return dict(obj)
        return super().default(obj)


class SharedHistory(models.Model):
    key = models.CharField(max_length=13, primary_key=True, verbose_name='Уникальный ключ по которому можно получить историю')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, null=False, blank=False, verbose_name='Пользователь, сохранивший статистику')
    from_date = models.DateField(verbose_name='Дата, начиная с которой будет показана история', null=True)
    to_date = models.DateField(verbose_name='Крайняя дата, по которую будет показана показана история', null=True)
    history_statistics = models.JSONField(encoder=CustomJSONEncoder, verbose_name='Сохраненная история пользователя по определенному промежутку времени')

    objects = DomainQuerySet.as_manager()


    class Meta:
        verbose_name = 'Закэшированная в базе данных история пользователя по определенному отрезку времени чтобы сохранить ее в быстром доступе и поделиться с другими пользователями'


    @classmethod
    def from_domain(cls, entity: SharedHistoryEntity):
        return cls(
            key=entity.key,
            user=User.from_domain(entity.user),
            from_date=entity.from_date,
            to_date=entity.to_date,
            history_statistics=entity.history_statistics
        )

    def to_domain(self):
        return SharedHistoryEntity(
            key=self.key,
            user=self.user.to_incomplete_domain(),
            from_date=self.from_date,
            to_date=self.to_date,
            history_statistics=self.history_statistics
        )

