from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserPasswordChangeForm, UserPasswordResetForm, UserPasswordResetConfirmForm
from task.mixins import TitleMixin


class UserRegistrationView(TitleMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'user/registration.html'
    title = 'Регистрация'


    def get_success_url(self):
        return reverse_lazy('user:login')


class UserLoginView(TitleMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'
    title = 'Аутентификация'


    def get_success_url(self):
        return reverse_lazy('user:profile')


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'user/profile.html'
    title = 'Профиль'


    def get_object(self, queryset = ...):
        return self.request.user
    

    def get_success_url(self):
        return reverse_lazy('user:profile')


class UserPasswordChangeView(TitleMixin, LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'user/password_change.html'
    title = 'Смена пароля'


    def get_success_url(self):
        return reverse_lazy('user:password_change_done')
    

class UserPasswordChangeDoneView(TitleMixin, PasswordChangeDoneView):
    template_name = 'user/password_change_done.html'
    title = 'Успешно'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('user:login')


class UserPasswordResetView(TitleMixin, PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'user/password_reset.html'
    email_template_name = 'user/password_reset_message.html'
    title = 'Сброс пароля'


    def get_success_url(self):
        return reverse_lazy('user:password_reset_done')


class UserPasswordResetDoneView(TitleMixin, PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'
    title = 'Сброс пароля'


class UserPasswordResetConfirmView(TitleMixin, PasswordResetConfirmView):
    form_class = UserPasswordResetConfirmForm
    template_name = 'user/password_reset_confirm.html'
    title = 'Сброс пароля'


    def get_success_url(self):
        return reverse_lazy('user:password_reset_complete')
    

    def render_to_response(self, context, **response_kwargs):
        '''
        Фреймворк принимает решение об отображении формы сброса пароля 
        на основе значения context['validlink']. Но в таком случае просто 
        отобразится та-же страница, но без формы. Я хочу возвращать именно
        403 статус, поэтому перехватываю это значение здесь. 
        '''
        if not context['validlink']:
            return HttpResponseForbidden('<h1>403 Недостаточно прав!</h1><p>Для посещения этой станицы требуется передать специальный одноразовый токен смены пароля!</p>')
        else:
            return super().render_to_response(context, **response_kwargs)


class UserPasswordResetCompleteView(TitleMixin, PasswordResetCompleteView):
    template_name = 'user/password_reset_complete.html'
    title = 'Успешно'


def check_user_status(request):
    return JsonResponse({'status': request.user.is_authenticated})
   
