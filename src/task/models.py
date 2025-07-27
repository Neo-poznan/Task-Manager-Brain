from django.db import models

from django.contrib.auth import get_user_model

from .domain.entities import CategoryEntity, TaskEntity
from user.models import User


class DomainQuerySet(models.QuerySet):
    def to_entity_list(self) -> list[TaskEntity]:
        return [task.to_domain() for task in self]


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Название категории')
    description = models.TextField(null=True, blank=True, verbose_name='Описание категории')
    color = models.CharField(max_length=40, null=False, blank=False, verbose_name='Цвет в формате rgb или rgba, который будет отображаться на статистике')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, null=True, blank=False, verbose_name='Пользователь, создавший категорию. Может быть пустым в случае, если категория создана автоматически')
    is_custom = models.BooleanField(null=False)

    objects = DomainQuerySet.as_manager()

    @classmethod
    def from_domain(cls, entity: CategoryEntity):
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            color=entity.color,
            user=User.from_domain(entity.user) if entity.user else None,
            is_custom=entity.is_custom
        )
    

    def to_domain(self) -> CategoryEntity:
        return CategoryEntity(
            id=self.id,
            name=self.name,
            description=self.description,
            color=self.color,
            user=self.user.to_domain() if self.user else None,
            is_custom=self.is_custom
        )


    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=290, null=False, blank=False, verbose_name='Название задачи')
    description = models.TextField(null=True, blank=True, verbose_name='Описание задачи')
    order = models.IntegerField(null=False, blank=False, verbose_name='Порядок задачи в списке')    
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Категория, к которой относится задача')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, null=False, blank=False, verbose_name='Пользователь, создавший задачу')
    deadline = models.DateField(null=True, blank=True, verbose_name='Крайний срок выполнения задачи')
    planed_time = models.DurationField(null=False, blank=False, verbose_name='Время, запланированное на процесс выполнения задачи')

    objects = DomainQuerySet.as_manager()


    @classmethod
    def from_domain(cls, entity: TaskEntity):
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            order=entity.order,
            category=Category.from_domain(entity.category),
            user=User.from_domain(entity.user),
            deadline=entity.deadline,
            planed_time=entity.planed_time
        )


    def to_domain(self) -> TaskEntity:
        return TaskEntity(
            id=self.id,
            name=self.name,
            description=self.description,
            order=self.order,
            category=self.category.to_domain(),
            user=self.user.to_domain(),
            deadline=self.deadline,
            planed_time=self.planed_time,
        )

