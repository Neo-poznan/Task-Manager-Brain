from django.shortcuts import render
from django.views.generic import View
from django.db import connection
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError

from task.mixins import TitleMixin, UserEntityMixin, LoginRequiredMixinWithRedirectMessage
from .services.use_cases import HistoryUseCase
from .infrastructure.database_repository import HistoryDatabaseRepository
from task.models import Task
from history.models import History
from .validators import history_query_params_validator, history_dates_interval_validator


class HistoryView(TitleMixin, LoginRequiredMixinWithRedirectMessage, UserEntityMixin, View):
    use_case = HistoryUseCase(HistoryDatabaseRepository(Task, History, connection))

    def get(self, request):
        try:
            from_date = self.request.GET['from_date']
            to_date = self.request.GET['to_date']
        except MultiValueDictKeyError:
            return HttpResponseBadRequest(
                '''
                <h1>400</h1>
                <p>Для запроса истории в ссылке должны быть переданы query-параметры, которые должны включать временной интервал, по которому будет показана история!</p>
                '''
            )
        try:
            history_query_params_validator(from_date, to_date)
            history_dates_interval_validator(from_date, to_date)
        except ValidationError as exc:
            return HttpResponseBadRequest(
                f'<h1>400</h1><p>{exc.message}</p>'
            )        


        context = self.use_case.get_user_history_statistics(self.get_user_entity(), from_date, to_date)
        context['title'] = 'История'
        return render(request, 'history/history.html', context=context)

