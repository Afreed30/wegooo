from django.shortcuts import render
from rest_framework import generics
from wegoooapp.models import User
from .serializers import UserSerializer
# Create your views here.
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

