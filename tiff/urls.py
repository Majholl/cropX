from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import UploadIMagePage , ShowImages , RotateImg , DeleteImg , UpdateAndSave 

urlpatterns = [

    path('' , UploadIMagePage , name='upload-image-page'),
    path('images/show-images' , ShowImages , name='show-image-page'),
    path('rotate/' , RotateImg , name='rotate-image'),
    path('remove/' , DeleteImg , name='remove-image'),
    path('reorder/' , UpdateAndSave , name='reoder-save')
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)