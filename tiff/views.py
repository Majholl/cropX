from urllib.request import Request
from django.shortcuts import render , redirect
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.conf import settings
from threading import Thread
import random , string , os , json 
from PIL import Image , ImageSequence


# These libraries are designed for different purposes.
from tiff.utils import write_in_storage , load_saved_images , handle_file_in_chnks





def home_page(request:Request) -> HttpResponse:
    "Render home page template"
    userid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    request.session['userid'] = userid
    return render(request, 'html/home.html', {})




def UploadImagePage(request:Request) -> HttpResponse:
    'Only render the index.html file for uploading tiff File'
    if request.method == 'POST':
        return render(request , 'html/uploadpage.html', {})
    
    return render(request , 'html/uploadpage.html' , {})







def ExtractingImages(request:Request) -> HttpResponse:
    
    """
        - Exctract img's inside the tiff file
        
    """
    try:
        if request.method != 'POST':
            return JsonResponse({'status' : 405 , 'msg':'method not supported'}) 
        
        ImageForm = request.FILES.get('tiff-image')  
        UserSessionId = request.session.get('userid')

        if ImageForm.content_type not in ['image/tiff' , 'image/x-tiff']:
            return render(request , 'html/wrongupload.html', {'status':415 , 'msg':'File not supported'}) 
            
        if not UserSessionId :
            return JsonResponse({'status': 400, 'data': 'Invalid session data'})

        ImagesPath = [] 
        MakeDirBaseOnUser = os.path.join(settings.MEDIA_ROOT, UserSessionId)
        os.makedirs(MakeDirBaseOnUser, exist_ok=True) 
                    
        TiffImagePath = os.path.join(MakeDirBaseOnUser, ImageForm.name) 
        write_in_storage(TiffImagePath, ImageForm)

        with Image.open(TiffImagePath) as opImg:
            for ind , page in enumerate(ImageSequence.Iterator(opImg) , 1):
                ImageFileName = f'{os.path.splitext(ImageForm.name)[0]}_page_{ind}.png'
                ImagePath = os.path.join(MakeDirBaseOnUser , ImageFileName)
                page.save(ImagePath , 'PNG' , optimize=True)
                ImagesPath.append(f"/media/{UserSessionId}/{ImageFileName}")
                
                
        request.session['tiffname'] = ImageForm.name
        request.session['imagesorder'] = ImagesPath 

        return redirect('show-images')
       
    except Exception as err:
        return render(request , 'html/wrongupload.html', {'status':500 , 'msg':'Internal server error'})
        
        
        
           
def ShowImages(request:Request) -> HttpResponse:
    """
        render image's into 'html/showimages.html'
    """
    try:
        UserSessionId = request.session.get('userid')
        ImagesPath = request.session['imagesorder']
        TiffFileName = request.session['tiffname']
        
        ImagesStored = os.path.join(settings.MEDIA_ROOT, UserSessionId)
        ImagesInsideStorage = os.listdir(ImagesStored)
        ImagesInsideStorage.remove(TiffFileName)
        
        for i in ImagesPath:
           if not str(os.path.normpath(i).split(os.sep)[-1]) in ImagesInsideStorage:
               return JsonResponse({'status':410 , 'data':'image not found , gone'})
                
        return render(request , 'html/showimages.html' , {'image_urls':ImagesPath})
    except Exception as err:
        
        return JsonResponse({'status':406 , 'data':'Not acceptable'})




def RotateImg(request:Request) -> HttpResponse:
          
    '''
        This section rotates the target IMG , saves it, 
        and returns the updated IMG  to the frontend.
    '''

    if request.method != 'POST':
        return JsonResponse({'status':405 , 'data':'request not allowed'}) 
    
    try:   
        
        AccessReqBody = json.loads(request.body) 
        ImagePath = AccessReqBody['imagepath']
        ImageAngle = AccessReqBody['imageangle']  
        BasedirMedia = settings.MEDIA_ROOT

        
        if not ImagePath or not ImageAngle:
            return JsonResponse({'status':406 , 'data':'Not acceptable , need image path and angle'})
                
        SplitPath = os.path.normpath(ImagePath).split(os.sep)
        ImagePathDir = os.path.join(BasedirMedia, SplitPath[-2], SplitPath[-1]) 

        OpenImage = Image.open(ImagePathDir)
        RotateImg = OpenImage.rotate(angle= -ImageAngle, expand=True, fillcolor=(255,255,255))
        RotateImg.save(ImagePathDir)
    
        ImageURL = f'/media/{SplitPath[-2]}/{SplitPath[-1]}'

        return JsonResponse({'status':200 , 'data' : ImageURL})
        
    except Exception as err:
        return JsonResponse({'status':500 , 'msg':'Internal server error'})








def DeleteImg(request):
    
    '''
        This section deletes the targeted IMG file from the frontend 
        and updates the order of the IMG's in the request session's imageorder.
    '''

    if request.method != 'POST':
        return JsonResponse({'status':405 , 'data':'request not allowed'}) 
    
    try: 
        BasedirMedia = settings.MEDIA_ROOT
        AccessReqBody = json.loads(request.body)
        ImagePath = AccessReqBody['imagepath']
        ImageOrder = request.session['imagesorder']

        if not ImagePath :
            return JsonResponse({'status':406 , 'data':'Not acceptable'})
        
        new_imageorderlist = []
        for i in ImageOrder:
            if i != str(ImagePath):
                new_imageorderlist.append(i)


        request.session['imagesorder'] = new_imageorderlist
        SplitPath = os.path.normpath(ImagePath).split(os.sep)  
        ImageURL = os.path.join(BasedirMedia , SplitPath[-2] , SplitPath[-1]) 

        if os.path.exists(ImageURL):
            os.remove(ImageURL) 
            
        
        return JsonResponse({'status':200 , 'data':f'{ImagePath}'}) 
        
    except Exception as err:
        return JsonResponse({'status':500 , 'msg':'Internal server error'})
             

    



def Reorder(request):
    '''
        This section receives any new recording from the frontend page, 
        and serves as the foundation for constructing the TIFF IMG file.
    '''

    if request.method != 'POST':
        return JsonResponse({'status':405 , 'data':'request not allowed'}) 
    

    try: 
        
        AccessReqBody = json.loads(request.body)   
        if not AccessReqBody['imageorder'] :
            return JsonResponse({'status':406 , 'data':'Not acceptable'})
        
        request.session['imagesorder'] = AccessReqBody['imageorder']
        
        return JsonResponse({'status':200 , 'data':'data reordered'})
        
    except Exception as err:
        return JsonResponse({'status':500 , 'msg':'Internal server error'})






def SaveAndDownload(request):
    '''
            Retrieve the request.session imageorder to find the paths of the IMG's, 
            then construct their paths and open the images using Pillow to serve the TIFF file.
                
            -- If any error occurs, return a JSON response including the `data` field.

            This section opens the IMG in TIFF format, splits it into pieces to
            efficiently serve the IMG's into memory, and then provides them for 
            download.
            
    '''
    if request.method !='POST':  
        return JsonResponse({'status': 405, 'msg': 'Request method not allowed'})
   
    
    try:
           

        BasedirMedia = settings.MEDIA_ROOT
        UserOrder = request.session.get('imagesorder')   
        UserSessionId = request.session.get('userid')
      
        if not UserOrder or not UserSessionId:
            return JsonResponse({'status': 400, 'data': 'Invalid session data'})

            
        check_files = os.path.join(BasedirMedia , UserSessionId)
        if not os.path.exists(check_files):
            return JsonResponse({'status': 404, 'data': 'User directory not found'})
           
           
        Images = []
        for images in UserOrder:
            splitImagePath = os.path.normpath(images).split(os.sep)
            UserImgpath = os.path.join(BasedirMedia , splitImagePath[2] , splitImagePath[3])
            Images.append(Image.open(UserImgpath))
  
        if not images:
            return JsonResponse({'status': 400, 'data': 'No valid images found'})

            
        NewFileName =  f'EditedImg.tiff'
        OutPutImg = os.path.join(BasedirMedia , UserSessionId  , NewFileName)
        Images[0].save(OutPutImg , save_all=True , append_images = Images[1:] , format="TIFF" , compression='tiff_deflate')

    except Exception as err:
        return JsonResponse({'status':103 , 'data':f"An error occurred while creating the new TIFF file {err}"})



    try:


        chunk_size = 1024 * 1024 # chunk size ; can be modified
        response = StreamingHttpResponse(handle_file_in_chnks(OutPutImg , chunk_size))
        response['Content-Disposition'] = f'attachment; filename="{NewFileName}"'
            
        return response
            
    except Exception as err:
        return JsonResponse({'status':500 , 'msg': f'Error while downlaoding File: {str(err)}'})    
    

    
