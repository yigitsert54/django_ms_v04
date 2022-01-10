from django.urls import path
from . import views

urlpatterns = [

    # FAQ main page
    path('faq/', views.faq, name="faq"),
    path('faq/<str:pk>/', views.single_topic, name="single_topic"),
    path('support/', views.support, name="support"),
    path('support/<str:pk>/', views.single_support, name="single_support"),
]
