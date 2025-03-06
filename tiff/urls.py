from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import UploadIMagePage , ExtractingImages , ShowImages , RotateImg ,  DeleteImg , Reorder ,  SaveAndDownload  


'''
    endpoint for rotating , remove and reordering images 
    - images/show-images/ : for showing extracted imgs
    - download/ : for download button
'''
urlpatterns = [
  
    path('', UploadIMagePage, name='upload-image-page'),
    path('extracting/', ExtractingImages, name='extracting-images-page'),
    path("images/", ShowImages, name="show-images"),
    path('rotate/', RotateImg, name='rotate-image'),
    path('remove/', DeleteImg, name='remove-image'),
    path('reorder/', Reorder, name='reoder') , 
    path('download/', SaveAndDownload, name='save-downlaod')
    
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)