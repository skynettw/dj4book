from django.contrib import admin
from django.urls import path
from mysite.views import about, listing, disp_detail, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about),
    path('list/', listing),
    path('list/<str:sku>/', disp_detail),
    path('', index)
]
