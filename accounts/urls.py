from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # Login & Logout
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),

    # Main Sidenav links
    path('dashboard/', views.dashboard, name="dashboard"),
    path('bookies/', views.bookies, name="bookies"),

    # Further bookie urls
    path('bookies/bookie/<str:pk>/', views.single_bookie, name="single_bookie"),
    path('add-bookie/', views.add_bookie, name="add_bookie"),
    path('deposit-money/<str:pk>/', views.deposit_money, name="deposit_money"),
    path('withdraw-money/<str:pk>/', views.withdraw_money, name="withdraw_money"),

    # Settings url
    path('settings/', views.settings, name="settings"),
    path('change-password/', views.change_password, name="change_password"),
    path('edit-account/', views.edit_account, name="edit_account"),
    path('edit-notifications/', views.edit_notifications,
         name="edit_notifications"),

    # New User
    path('digistore-registration/', views.digistore_registration,
         name="digistore_registration"),

    # password reset views
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="password_reset"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]
