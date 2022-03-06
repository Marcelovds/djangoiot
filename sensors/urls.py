from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<slug:slug>', views.sensor_detail, name='sensor_detail'),
    path('api/data/<slug:slug>', views.api_add_data, name='sensor_add_data'),
]

