from django.urls import path
from . import views
urlpatterns = [
    path('user/',views.UserListCreateAPIView.as_view(), name='user-list-create'),
    ]