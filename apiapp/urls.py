from django.urls import path
from .views import get_file, rotate_img, delete_img, reorder_img, download_file





urlpatterns = [
    path('upload/', get_file, name='Upload-file'),
    path('rotate/', rotate_img, name='Rotate-imgs'),
    path('delete/', delete_img, name='Delete-imgs'),
    path('reorder/', reorder_img, name='Reorder-imgs'),
    path('download/<str:id>/<str:filename>', download_file, name='Download-file')
]