from django.db import models
from django.contrib.auth import get_user_model

from task.models import Category, DomainQuerySet
from user.models import User
from .domain.entities import HistoryEntity


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

