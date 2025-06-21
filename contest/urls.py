from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_supabase_contests, name='show_supabase_contests'),
]
