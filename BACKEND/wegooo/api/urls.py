from django.urls import path
from . import views
urlpatterns = [
    path('buses/', views.BusList.as_view(), name='bus-list'),]