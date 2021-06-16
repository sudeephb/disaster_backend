from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    # path('<label>/', views.selected_disaster, name = 'selected_disasters')
]
