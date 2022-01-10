from django.urls import path
from . import views

urlpatterns = [
    path('bets/<str:type>/', views.bets, name="bets"),
    path('valuebets/', views.value_matches, name="value_bets"),
    path('performance/', views.performance, name="performance"),

    path('add-matches/', views.add_matches, name="add_matches"),
    path('update-matches/', views.update_matches, name="update_matches"),
    path('open-matches-ids/', views.get_open_matches, name="get_open_matches"),
]
