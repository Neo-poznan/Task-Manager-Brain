from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.db import connection

from .mixins import TitleMixin, UserEntityMixin, LoginRequiredMixinWithRedirectMessage
from .forms import TaskCreationForm, CategoryCreationForm, TaskHistoryForm
from .models import Task, Category
from .services.use_cases import TaskUseCase
from .infrastructure.database_repository import TaskDatabaseRepository, CategoryDatabaseRepository
from .serializers import to_json, from_json
from history.infrastructure.database_repository import HistoryDatabaseRepository
from history.models import History, SharedHistory


class MyTasksView(LoginRequiredMixinWithRedirectMessage, UserEntityMixin, TitleMixin, TemplateView):
    title = 'Мои задачи'
    template_name = 'task/index.html'
    use_case = TaskUseCase(task_database_repository=TaskDatabaseRepository(Task, connection))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['chart_data'] = to_json(self.use_case.get_user_task_count_statistics(self.get_user_entity()))
        context['calendar_data'] = to_json(self.use_case.get_count_user_tasks_in_categories_by_deadlines(self.get_user_entity()))
        context['task_list'] = self.use_case.get_ordered_user_tasks(self.get_user_entity())
        return context

class TaskCreationView(LoginRequiredMixinWithRedirectMessage, UserEntityMixin, TitleMixin, CreateView):
    form_class = TaskCreationForm
    title = 'Создание задачи'
    template_name = 'task/task.html'
    success_url = reverse_lazy('task:my_tasks')

    def form_valid(self, form):
        use_case = TaskUseCase(task_database_repository=TaskDatabaseRepository(Task, connection))        
        form.instance.order = use_case.get_next_task_order(self.get_user_entity())
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryCreationView(LoginRequiredMixinWithRedirectMessage, UserEntityMixin, TitleMixin, CreateView):
    form_class = CategoryCreationForm
    title = 'Создание категории'
    template_name = 'task/category.html'
    success_url = reverse_lazy('task:categories')
    use_case = TaskUseCase()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['default_color'] = self.use_case.get_random_hex_color()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_custom = True
        form.instance.color = self.use_case.get_rgba_color_with_default_obscurity(form.cleaned_data.get('color'))
        return super().form_valid(form)
    

class TaskUpdateView(LoginRequiredMixinWithRedirectMessage, UserEntityMixin, TitleMixin, UpdateView):
    form_class = TaskCreationForm
    title = 'Просмотр и изменение задачи'
    template_name = 'task/task.html'
    success_url = reverse_lazy('task:my_tasks')
    use_case = TaskUseCase(task_database_repository=TaskDatabaseRepository(Task, connection))

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('<h1>404 Not Found</h1><p>Такой задачи не существует</p>')
        except PermissionError:
            return HttpResponseForbidden('<h1>400 Forbidden</h1><p>Вы пытаетесь отредактировать задачу другого пользователя</p>')

    def get_initial(self):
        initial = super().get_initial()
        initial['deadline'] = str(self.get_object().deadline)
        return initial

    def get_object(self):
        return Task.from_domain(self.use_case.get_user_task_by_id(task_id=self.kwargs.get('task_id'), user=self.get_user_entity()))


class CategoryUpdateView(LoginRequiredMixinWithRedirectMessage, UserEntityMixin, TitleMixin, UpdateView):
    form_class = CategoryCreationForm
    title = 'Просмотр и изменение категории'
    template_name = 'task/category.html'
    success_url = reverse_lazy('task:categories')
    use_case = TaskUseCase(category_database_repository=CategoryDatabaseRepository(Category))

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('<h1>404 Not Found</h1><p>Такой категории не существует</p>')
        except PermissionError:
            return HttpResponseForbidden('<h1>400 Forbidden</h1><p>Вы пытаетесь отредактировать категорию другого пользователя или системную категорию</p>')

    def form_valid(self, form):
        form.instance.color = self.use_case.get_rgba_color_with_default_obscurity(form.cleaned_data.get('color'))
        return super().form_valid(form)

    def get_object(self):
        return Category.from_domain(self.use_case.get_user_category_by_id(category_id=self.kwargs.get('category_id'), user=self.get_user_entity()))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['default_color'] = self.use_case.get_hex_color_by_category_id(self.kwargs.get('category_id'))
        return context
        

class CategoryDeletionView(LoginRequiredMixinWithRedirectMessage, UserEntityMixin, DeleteView):
    use_case = TaskUseCase(category_database_repository=CategoryDatabaseRepository(Category))

    def dispatch(self, request, *args, **kwargs):
        try:
            if self.request.method != 'DELETE':
                return HttpResponseBadRequest('<h1>Bab Request</h1><p>Неправильный метод запроса</p>')
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('<h1>404 Not Found</h1><p>Такой категории не существует</p>')
        except PermissionError:
            return HttpResponseForbidden('<h1>403 Forbidden</h1><p>Вы пытаетесь удалить категорию другого пользователя или системную категорию</p>')   

    def delete(self, request, *args, **kwargs):
        self.use_case.delete_user_category_by_id(self.kwargs.get('category_id'), self.get_user_entity())
        return JsonResponse({'redirect_url': reverse_lazy('task:categories')}, status=203)


class CategoriesView(LoginRequiredMixinWithRedirectMessage, UserEntityMixin, TitleMixin, TemplateView):
    template_name = 'task/categories.html'
    title = 'Категории'
    use_case = TaskUseCase(category_database_repository=CategoryDatabaseRepository(Category))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories_list'] = self.use_case.get_ordered_user_categories(self.get_user_entity())
        return context
    

class OrderUpdateView(LoginRequiredMixinWithRedirectMessage, UserEntityMixin, View):

    def get(self, request):
        return HttpResponseBadRequest('<h1>Bab Request</h1><p>Неправильный метод запроса</p>')
    
    def put(self, request):
        post_data = self.request.body.decode('utf-8')
        post_data_json = from_json(post_data)
        use_case = TaskUseCase(task_database_repository=TaskDatabaseRepository(Task, connection))
        use_case.update_user_task_order(self.get_user_entity(), post_data_json['order'])
        return HttpResponse('OK')


class TaskCompletionView(LoginRequiredMixinWithRedirectMessage, UserEntityMixin, TitleMixin, View):
    title = 'Подтверждение выполнения задачи'

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionError:
            return HttpResponseForbidden('<h1>400 Forbidden</h1><p>Вы пытаетесь удалить задачу другого пользователя</p>')

    def get(self, request, task_id: int):
        return render(
            request, 
            'task/save_task_to_history.html',
            context={'form': TaskHistoryForm(), 'label': 'Сколько времени вам понадобилось на процесс выполнения непосредственно этой задачи'}
        )

    def post(self, request, task_id: int):
        use_case = TaskUseCase(
            task_database_repository=TaskDatabaseRepository(Task, connection),
            history_database_repository=HistoryDatabaseRepository(Task, History, SharedHistoryStatistics, connection)
        )
        use_case.save_completed_task_to_history(self.get_user_entity(), task_id, self.request.POST['execution_time'])
        return HttpResponseRedirect(reverse_lazy('task:my_tasks'))
    

class TaskFailView(LoginRequiredMixinWithRedirectMessage, UserEntityMixin, TitleMixin, View): 
    title = 'Подтверждение провала задачи'

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionError:
            return HttpResponseForbidden('<h1>400 Forbidden</h1><p>Вы пытаетесь удалить задачу другого пользователя</p>')

    def get(self, request, task_id: int):
        return render(
            request,
            'task/save_task_to_history.html', 
            context={'form': TaskHistoryForm(), 'label': 'Сколько времени вам понадобилось на то, чтобы понять, что вы не сможете выполнить задачу'}
        )

    def post(self, request, task_id: int):
        use_case = TaskUseCase(
            task_database_repository=TaskDatabaseRepository(Task, connection),
            history_database_repository=HistoryDatabaseRepository(Task, History, SharedHistory, connection)
        )
        use_case.save_failed_task_to_history(self.get_user_entity(), task_id, self.request.POST['execution_time'])

        return HttpResponseRedirect(reverse_lazy('task:my_tasks'))
    
