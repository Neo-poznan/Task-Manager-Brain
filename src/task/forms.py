from django import forms

from .models import Task as Task
from .models import Category as Category


class TaskCreationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'name-id-for-label',
            'placeholder': 'Название...',
        }),
        label='Название задачи'
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'description-id-for-label',
            'placeholder': 'Описание... (можно Markdown)',
        }),
        required=False,
        label='Описание задачи (необязательно)'
    )

    deadline = forms.DateField(
        widget=forms.DateInput(attrs={''
            'type': 'date',
            'id': 'deadline-id-for-label',
        }),
        required=False,
        label='Крайняя дата выполнения задачи (необязательно)'
    )

    planed_time = forms.DurationField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'id': 'planed-time-id-for-label',
            'step': '1',

        }),
        label = 'Планируемое время на процесс выполнения задачи (будет округлено до десятков минут)'
    )


    class Meta:
        model = Task
        fields = ['name', 'description', 'category', 'deadline', 'planed_time']


class CategoryCreationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'name-id-for-label',
            'placeholder': 'Название',
        }),
        required=True,
        label='Название категории'
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'description-id-for-label',
            'placeholder': 'Описание... (можно Markdown)',
        }),
        required=False,
        label='Описание категории (необязательно)'
    )
    
    color = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'color',
            'id': 'color-id-for-label',
        }),
        label='Цвет категории на диаграмме'
    )


    class Meta:
        model = Category
        fields = ['name', 'description', 'color']

