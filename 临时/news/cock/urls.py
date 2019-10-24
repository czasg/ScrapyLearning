from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('api/get/map/data', api_get_map_data),
    path('api/get/map/data/v1', api_get_map_data_v1),
]
