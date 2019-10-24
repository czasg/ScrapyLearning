from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('api/get/map/data', api_get_map_data),
]
