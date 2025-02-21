from django.shortcuts import render
from django.http import JsonResponse , FileResponse
from django.conf import settings
from threading import Thread
import random , string , os , json
from PIL import Image 
from time import time
from .utils.utils import write_in_storage , load_saved_images , StreamDownloadFile
import zipfile


def UploadIMagePage(request):
    userId = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    request.session['userid'] = userId

    if request.method == 'POST':
        return render(request , 'html/index.html', {'userId':userId})
    
    return render(request , 'html/index.html' , {'userId' : userId})






def ShowImages(request):
    ImageForm = request.FILES.get('tiff-image')
    UserSessionId = request.session.get('userid')

    if not ImageForm :
        return JsonResponse({'status':400 , 'msg':'File not Uploaded'})
    
    if ImageForm.content_type not in ['image/tiff' , 'image/x-tiff']:
        return JsonResponse({'status':415 , 'msg':'File not supported'})
    
    MakeDirBaseOnUser = os.path.join(settings.MEDIA_ROOT , UserSessionId)
    os.makedirs(MakeDirBaseOnUser , exist_ok=True)

    TiffImagePath = os.path.join(MakeDirBaseOnUser , ImageForm.name)
    write_in_storage(TiffImagePath , ImageForm)

    ImagesPath = []
    thread = Thread(target=load_saved_images , args=(TiffImagePath , ImageForm , MakeDirBaseOnUser , UserSessionId , ImagesPath))
    thread.start()
    thread.join()
    
    return render(request , 'html/showimages.html' , {'image_urls':ImagesPath})




def RotateImg(request):
    if request.method == 'POST':
        AccessReqBody = json.loads(request.body)
        BasedirMedia = settings.MEDIA_ROOT

        SplitPath = AccessReqBody['imagepath'].split('/')
        ImagePath = os.path.join(BasedirMedia , SplitPath[2] , SplitPath[3])
        ImageAngle = AccessReqBody['imageangle']

        OpenImage = Image.open(ImagePath)
        RotateImg = OpenImage.rotate(angle=ImageAngle , expand=True)
        RotateImg.save(ImagePath)

        ImageURL = f'/media/{SplitPath[2]}/{SplitPath[3]}'
        return JsonResponse({'status':200 , 'data' : ImageURL})
    
    else:
        return JsonResponse({'status':405 , 'msg':'request not allowed'})
    




def DeleteImg(request):
    if request.method =='POST':
        AccessReqBody = json.loads(request.body)
        BasedirMedia = settings.MEDIA_ROOT

        SplitPath = AccessReqBody['imagepath'].split('/')
        ImagePath = os.path.join(BasedirMedia , SplitPath[2] , SplitPath[3])
        os.remove(ImagePath)

        return JsonResponse({'status':200 , 'data':f'{ImagePath} removed successfully'})
    
    else:
        return JsonResponse({'status':405 , 'msg':'request not allowed'})
    




def UpdateAndSave(request):
    if request.method =='POST':
        AccessReqBody = json.loads(request.body)
        BasedirMedia = settings.MEDIA_ROOT
        UserImgpath = os.path.join(BasedirMedia , request.session['userid'])
        ImagePath =[]
        if not AccessReqBody['imagepath']:
            for images in os.listdir(UserImgpath)[1:]:
                GenerateImgPath = os.path.join(UserImgpath , images)
                ImagePath.append(GenerateImgPath)
        
        
        for i in AccessReqBody['imagepath']:
            SplitPath = i.split('/')
            GenerateImgPath = os.path.join(BasedirMedia , SplitPath[2] , SplitPath[3])
            ImagePath.append(GenerateImgPath)

       
        Imagess = [Image.open(ImagePath[0])]
        for path in ImagePath[1:]:
            Imagess.append(Image.open(path))
        NewFileName =  f'EditedImg.tiff'
        OutPutImg = os.path.join(UserImgpath , NewFileName)

        try:
            Imagess[0].save(OutPutImg , save_all=True , append_images = Imagess[1:] , format="TIFF" , compression='tiff_deflate')
            response = FileResponse(open(OutPutImg , 'rb'), as_attachment=True, content_type='image/tiff')
            response['Content-Disposition'] = f'attachment; filename="{NewFileName}"'
            
            return response
        
        except Exception as err:
            return JsonResponse({'status':500 , 'msg': f'Error while downlaoding File: {str(err)}'})    
    
    
    return JsonResponse({'status': 405, 'msg': 'Request method not allowed'})
   
    
    
