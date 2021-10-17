from django.urls import path
from . import views

app_name = 'chromatography'
urlpatterns = [
    path('', views.all_chrommodels, name='all_chrommodels'),
    path('<int:y>/<int:m>/<int:d>/<slug:slug>/', views.detailed_chrommodel,
         name='detailed_chrommodel'),
]