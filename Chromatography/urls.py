from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'chromatography'
urlpatterns = [

    path('', views.all_models, name='all_models'),
    path('logp/', views.all_logpmodels, name='all_logpmodels'),
    path('lser/', views.all_lsermodels, name='all_lsermodels'),
    path('detailed_logp/<int:y>/<int:m>/<int:d>/<slug:slug>/', views.detailed_logpmodel,
         name='detailed_logpmodel'),
    path('detailed_lser/<int:y>/<int:m>/<int:d>/<slug:slug>/', views.detailed_lsermodel,
         name='detailed_lsermodel'),
    path('detailed_column/<int:y>/<int:m>/<int:d>/<slug:slug>/', views.detailed_column,
         name='detailed_column'),
    path('create_logp_model/', views.create_logp_model, name='create_logpmodel'),
    path('create_lser_model/', views.create_lser_model, name='create_lsermodel'),
    path('columns/', views.all_columns, name='all_columns'),
    path('create_column/', views.create_column, name='create_column'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
