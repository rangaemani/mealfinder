from django.shortcuts import render
from rest_framework import viewsets
from .serializers import MealSerializer
from .models import Meal
from django.http import JsonResponse
import requests

# Create your views here.

def search_meals(request):
    print(request.GET)
    ingredient = request.GET.get('ingredient')
    cuisine = request.GET.get('cuisine')

    if (not ingredient or ingredient.strip() == "") and (not cuisine or cuisine.strip() == ""):
        return JsonResponse({'error': 'No ingredient or cuisine provided'}, status=400)

    if ingredient and ingredient.strip() != "":
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
    else:
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={cuisine}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        meals = data.get('meals')

        response = JsonResponse({'meals': meals})
        response['access-control-allow-origin'] = 'http://localhost:8000'
        return response

    return JsonResponse({'error': 'API request failed'}, status=500)

class MealView(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    queryset = Meal.objects.all()