from rest_framework import generics, permissions
from .serializers import OrganizerRegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = OrganizerRegisterSerializer
    permission_classes = [permissions.AllowAny]
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
