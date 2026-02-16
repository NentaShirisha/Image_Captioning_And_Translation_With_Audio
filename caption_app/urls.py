from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload, name='upload'),
    path('history/', views.history, name='history'),
    path('profile/', views.profile, name='profile'),
    path('generate/', views.generate_caption_view, name='generate_caption'),
    path('api/generate-caption/', views.CaptionAPI.as_view(), name='api_generate_caption'),
]