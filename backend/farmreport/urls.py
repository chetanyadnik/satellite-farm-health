from django.urls import path
from .views import process_polygon

urlpatterns = [
    path('process-polygon/', process_polygon),
]
