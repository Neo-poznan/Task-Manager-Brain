from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('change-password/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('change-password/success/', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('reset-password/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('reset-password/success/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('check-status/', views.check_user_status)
]

