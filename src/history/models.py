from django.db import models
from django.contrib.auth import get_user_model

from task.models import Category


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


    class Meta:
        verbose_name = 'История выполненных и проваленных задач. Одна строка - одна задача.'

