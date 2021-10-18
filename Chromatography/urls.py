from django.urls import path
from . import views

app_name = 'chromatography'
urlpatterns = [
    path('', views.all_logpmodels, name='all_logpmodels'),
    path('<int:y>/<int:m>/<int:d>/<slug:slug>/', views.detailed_logpmodel,
         name='detailed_logpmodel'),
    # path('calculate/', views.calculate_retention_time, name='calculate'),
]