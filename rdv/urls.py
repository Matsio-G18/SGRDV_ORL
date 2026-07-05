from django.urls import path
from . import views

app_name = 'rdv'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list_rdv, name='list'),
    path('notifications/', views.notifications, name='notifications'),
    path('<int:id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('<int:id>/delete/', views.delete, name='delete'),
]
