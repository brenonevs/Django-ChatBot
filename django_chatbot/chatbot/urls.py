from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("chatbot/", views.ChatbotView.as_view(), name="chatbot"),
]
