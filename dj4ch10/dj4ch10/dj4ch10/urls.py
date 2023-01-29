from django.contrib import admin
from django.urls import path, include
from mysite import views
from django.conf import settings
from django.conf.urls.static import static 

admin.site.site_header = "我的私人日記"
admin.site.site_title = "我的私人日記"
admin.site.index_title = "我的私人日記後台"


urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('logout/', views.logout),
    path('userinfo/', views.userinfo),
    path('post/', views.posting),
    path('accounts/', include('registration.backends.default.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
