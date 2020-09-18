from django.urls import path
from chart import views


app_name = 'chart'
urlpatterns = [
    path('Line-chart', views.main_view, name='Line-chart'),
]