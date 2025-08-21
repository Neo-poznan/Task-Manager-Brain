from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist

from .domain.entities import UserEntity
from .validators import email_validator


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_images', default='user_images/default_avatar.png')
    first_name = None
    last_name = None
    is_superuser = None
    is_staff = None


    @classmethod
    def from_domain(cls, entity: UserEntity):
        return cls(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            password=entity.password,
            last_login=entity.last_login,
            is_active=entity.is_active,
            date_joined=entity.date_joined
        )
    

    def to_domain(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            last_login=self.last_login,
            is_active=self.is_active,
            date_joined=self.date_joined
        )
    

    def clean(self):
        try:
            if User.objects.get(id=self.id).email == self.email:
                return
        except ObjectDoesNotExist:
            pass

        email_validator(self.email)

    
    class Meta:
        verbose_name = '''
            Пользователи системы. Тут нет разделения на роли, роль одна - обычный пользователь. 
            Никто не имеет права просматривать и изменять информацию другого пользователя.
        '''

