from django.urls import path
from . import views

from .views import CustomLoginView

urlpatterns = [

    path('', views.home),
    path('clients/', views.client_list),
    path('clients/<int:pk>/', views.client_detail),
    path('clients/<int:client_id>/projects/', views.create_project),
    path('projects/', views.user_projects),
    path('api/login/', CustomLoginView.as_view(), name='login'),
]