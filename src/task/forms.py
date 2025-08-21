from datetime import timedelta
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

    planned_time = forms.DurationField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'id': 'planned-time-id-for-label',
            'step': '1',

        }),
        label = 'Планируемое время на процесс выполнения задачи (будет округлено до десятков минут)'
    )


    def clean_planned_time(self):
        '''
        Округляет планируемое время выполнения до десятков минут.
        Называется так, потому что форма вызывает только такие названия
        '''
        planned_time_str = str(self.cleaned_data.get('planned_time'))
        planned_time_hours = planned_time_str.split(':')[0]
        planned_time_minutes = planned_time_str.split(':')[1]
        rounded_planned_time_ten_minutes = planned_time_minutes[0] if int(planned_time_minutes[1]) < 5 else str(int(planned_time_minutes[0]) + 1)
        return timedelta(hours=int(planned_time_hours), minutes=int(rounded_planned_time_ten_minutes + '0'))


    class Meta:
        model = Task
        fields = ['name', 'description', 'category', 'deadline', 'planned_time']


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



class TaskHistoryForm(forms.Form):
    execution_time = forms.DurationField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'id': 'execution-time-id-for-label',
            'step': '1',

        })
    )


