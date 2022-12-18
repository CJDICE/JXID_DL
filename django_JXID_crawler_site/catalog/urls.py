from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_index, name='show_index'),
    path('submit/', views.submit, name='submit'),
    path('success/', views.success_view, name='success'),
]