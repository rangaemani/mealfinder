import os
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import MealSerializer
from .models import Meal
from django.http import JsonResponse
import requests

def search_meals(request):
    ## request debugging
    print(request.GET)
    ## parse api query keys
    searchDB = request.GET.get('searchDB')
    ingredient = request.GET.get('ingredient')
    cuisine = request.GET.get('cuisine')
    ## error checking
    if (not ingredient or ingredient.strip() == "") and (not cuisine or cuisine.strip() == ""):
        return JsonResponse({'error': 'No ingredient or cuisine provided'}, status=400)
    if searchDB == 'TheMealDB':
        ## conditional api url setup
        if ingredient and ingredient.strip() != "":
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
        else:
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={cuisine}"

        response = requests.get(url)

        ## response population
        if response.status_code == 200:
            data = response.json()
            meals = data.get('meals')
            response = JsonResponse({'meals': meals})
            response['access-control-allow-origin'] = 'http://localhost:8000'
            return response
        ## error handling
        return JsonResponse({'error': 'API request failed'}, status=500)
    elif searchDB == 'EDAMAM':
        app_id = os.getenv('APP_ID')
        app_key = os.getenv('APP_KEY')
        ## conditional api url setup
        if ingredient and ingredient.strip() != "":
            url = f"https://api.edamam.com/api/recipes/v2?type=public&q={ingredient}&app_id={app_id}&app_key={app_key}"
        else:
            url = f"https://api.edamam.com/api/recipes/v2?type=public&app_id={app_id}&app_key={app_key}&cuisineType={cuisine}"

        response = requests.get(url)

        ## response population
        if response.status_code == 200:
            data = response.json()
            meals = data.get('hits')
            response = JsonResponse({'meals': meals})
            response['access-control-allow-origin'] = 'http://localhost:8000'
            return response
        ## error handling
        return JsonResponse({'error': 'API request failed'}, status=500)

## serializing meal data using predefined object schema
class MealView(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    queryset = Meal.objects.all()