from django.urls import path
from django.contrib import admin
from mysite.views import homepage, showpost

urlpatterns = [
    path('', homepage),
    path('post/<slug:slug>/', showpost),
    path('admin/', admin.site.urls),
]
