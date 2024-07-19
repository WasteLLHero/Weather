from django.contrib import admin
from django.urls import path
from weatherapi import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.WeatherListView.as_view(), name='weather'),
    path('cities/', views.CityList.as_view()),

]
