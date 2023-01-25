from django.contrib import admin
from django.urls import path, include
from mysite import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('delpost/<int:pid>/<str:del_pass>/', views.delpost),
    path('list/', views.listing),
    path('post/', views.posting),
    path('contact/', views.contact),
    path('post2db/', views.post2db),
    path('bmi/', views.bmi),
    path('captcha/', include('captcha.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
