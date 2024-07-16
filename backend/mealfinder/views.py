from django.shortcuts import render
from rest_framework import viewsets
from .serializers import MealSerializer
from .models import Meal

# Create your views here.

class MealView(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    queryset = Meal.objects.all()