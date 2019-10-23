from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('api/get/china/map/data', api_get_china_map_data),
    path('api/get/world/cloud/data', api_get_world_cloud_data),
    path('api/get/map/data', api_get_map_data),
]
