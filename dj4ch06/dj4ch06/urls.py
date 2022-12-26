from django.contrib import admin
from django.urls import path
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('engtv/', views.engtv),
    path('engtv/<int:tvno>/', views.engtv, name='engtv-url'),
    path('carlist/', views.carlist),
    path('carlist/<int:maker>/', views.carlist, name='carlist-url'),
    path('carprice/', views.carprice),
    path('carprice/<int:maker>/', views.carprice, name='carprice-url'),
    path('<int:tvno>/', views.index, name = 'tv-url')
]
