from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection

from task.mixins import TitleMixin, UserEntityMixin
from .services.use_cases import HistoryUseCase
from .infrastructure.database_repository import HistoryDatabaseRepository
from task.models import Task
from history.models import History


class HistoryView(TitleMixin, LoginRequiredMixin, UserEntityMixin, View):
    use_case = HistoryUseCase(HistoryDatabaseRepository(Task, History, connection))

    def get(self, request):
        context = self.use_case.get_user_history_statistics(self.get_user_entity())
        context['title'] = 'История'
        return render(request, 'history/history.html', context=context)

