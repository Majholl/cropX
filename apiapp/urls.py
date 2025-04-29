from django.urls import path
from .views import get_file, rotate_img, delete_img





urlpatterns = [
    path('upload/', get_file, name='Upload-file'),
    path('rotate/', rotate_img, name='Rotate-imgs'),
    path('delete/', delete_img, name='Delete-imgs'),
]