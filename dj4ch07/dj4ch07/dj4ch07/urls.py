from django.contrib import admin
from django.urls import path
from mysite import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('detail/<int:id>', views.detail, name = 'detail-url'),
    path('', views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
