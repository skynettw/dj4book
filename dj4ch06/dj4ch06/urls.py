from django.contrib import admin
from django.urls import path
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('<int:tvno>/', views.index, name = 'tv-url')
]
