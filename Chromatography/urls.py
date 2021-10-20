from django.urls import path
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
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
