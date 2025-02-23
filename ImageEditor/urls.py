from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('tiff.urls')) # this include url's of  tiff app 
]
