from django.shortcuts import render
from django.http import JsonResponse , StreamingHttpResponse
from django.conf import settings
from threading import Thread
import random , string , os , json , time
from PIL import Image 

# These libraries are designed for different purposes.
from tiff.utils import write_in_storage , load_saved_images , handle_file_in_chnks





def UploadIMagePage(request):
    
    '''
        Only render the index.html file for uploading tiff IMG
    '''
    userId = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    request.session['userid'] = userId
     
    if request.method == 'POST':
        return render(request , 'html/index.html', {'userId':userId})
    
    return render(request , 'html/index.html' , {'userId' : userId})





def ShowImages(request):
    
    if request.method == 'POST':
            
        ImageForm = request.FILES.get('tiff-image') 
        UserSessionId = request.session.get('userid')

        if not ImageForm :
            return render(request , 'html/notuploaded.html' ,{'status':400 , 'msg':'File not Uploaded'}) #
        
        if ImageForm.content_type not in ['image/tiff' , 'image/x-tiff']:
            return render(request , 'html/notuploaded.html', {'status':415 , 'msg':'File not supported'}) 
        
        try:
            '''
                This section extracts TIFF IMG's, saves them, 
                and serves them to the frontend.

                --uses another thread for faster IMG's loading

            '''

            MakeDirBaseOnUser = os.path.join(settings.MEDIA_ROOT , UserSessionId) 
            os.makedirs(MakeDirBaseOnUser , exist_ok=True) 
            
            TiffImagePath = os.path.join(MakeDirBaseOnUser , ImageForm.name) 
            write_in_storage(TiffImagePath , ImageForm)

            
            ImagesPath = [] # shared list with other thread(core/ process) to access image's extracted 
            thread = Thread(target=load_saved_images , args=(TiffImagePath , ImageForm , MakeDirBaseOnUser , UserSessionId , ImagesPath))
            thread.start()
            thread.join() # end of the thread activity 
            request.session['tiffname'] = ImageForm.name
            request.session['imagesorder'] = ImagesPath 
            
        except Exception as err:
            return render(request , 'html/notupladed.html', {'status':500 , 'msg':'server side error back to upload page'})
        
        return render(request , 'html/showimages.html' , {'image_urls':ImagesPath})
    
    else:
        return JsonResponse({'status' : 405 , 'msg':'method not supported'}) 






def RotateImg(request):
    if request.method == 'POST':
        try:   
            
            '''
                This section rotates the target IMG , saves it, 
                and returns the updated IMG  to the frontend.
            '''
            BasedirMedia = settings.MEDIA_ROOT
            try:   
                AccessReqBody = json.loads(request.body) 
                ImagePath = AccessReqBody['imagepath']
                ImageAngle = AccessReqBody['imageangle']  
            except Exception as err:
                    return JsonResponse({'status':100 , 'data':'Need info , lack of Imagepath or ImageAngle'})
                

            SplitPath = os.path.normpath(ImagePath).split(os.sep)
            ImagePathDir = os.path.join(BasedirMedia , SplitPath[2] , SplitPath[3]) 

            OpenImage = Image.open(ImagePathDir)
            RotateImg = OpenImage.rotate(angle=ImageAngle , expand=True)
            RotateImg.save(ImagePathDir)

            ImageURL = f'/media/{SplitPath[2]}/{SplitPath[3]}' 
            
            return JsonResponse({'status':200 , 'data' : ImageURL})
        
        except Exception as err:
            return JsonResponse({'status':500 , 'data':'server side error back to upload page '})
      
    else:
        return JsonResponse({'status':405 , 'data':'request not allowed'}) 
    



def DeleteImg(request):
    if request.method =='POST':
        AccessReqBody = json.loads(request.body)
        BasedirMedia = settings.MEDIA_ROOT
        try: 
            '''
                This section deletes the targeted IMG file from the frontend 
                and updates the order of the IMG's in the request session's imageorder.
            '''

            ImagePath = AccessReqBody['imagepath']
            ImageOrder = request.session['imagesorder']
            
            new_imageorderlist = []
            for i in ImageOrder:
                if i != str(ImagePath):
                    new_imageorderlist.append(i)
            request.session['imagesorder'] = new_imageorderlist

            SplitPath = os.path.normpath(ImagePath).split(os.sep) 
            ImagePath = os.path.join(BasedirMedia , SplitPath[2] , SplitPath[3]) 

            os.remove(ImagePath) 
            return JsonResponse({'status':200 , 'data':f'{ImagePath} removed successfully'}) 
        
        except Exception as err:
           return JsonResponse({'status':500 , 'data':'server side error back to upload page '})
             
    else:
        return JsonResponse({'status':405 , 'data':'request not allowed'}) 
    




def Reorder(request):
    if request.method == 'POST':
        try:
            '''
                This section receives any new recording from the frontend page, 
                and serves as the foundation for constructing the TIFF IMG file.
            '''

            AccessReqBody = json.loads(request.body)
            
            request.session['imagesorder'] = AccessReqBody['imageorder']
            return JsonResponse({'status':200 , 'data':'data reordered'})
        
        except Exception as err:
            return JsonResponse({'status':404 , 'data':'data not found'}) 
            
    else:
        return JsonResponse({'status':405 , 'data':'request not allowed'}) 
    




def SaveAndDownload(request):
    if request.method =='POST':
        try:
            '''
                Retrieve the request.session imageorder to find the paths of the IMG's, 
                then construct their paths and open the images using Pillow to serve the TIFF file.
                
                -- If any error occurs, return a JSON response including the `data` field.
            '''

            BasedirMedia = settings.MEDIA_ROOT
            UserOrder = request.session['imagesorder']
            
            UserSessionId = request.session.get('userid')
            Images = []
            for images in UserOrder:
                splitImagePath = os.path.normpath(images).split(os.sep)
                UserImgpath = os.path.join(BasedirMedia , splitImagePath[2] , splitImagePath[3])
                Images.append(Image.open(UserImgpath))
  
            NewFileName =  f'{int(time.time())}_EditedImg.tiff'
            OutPutImg = os.path.join(BasedirMedia , UserSessionId  , NewFileName)
            Images[0].save(OutPutImg , save_all=True , append_images = Images[1:] , format="TIFF" , compression='tiff_deflate')

        except Exception as err:
            return JsonResponse({'status':103 , 'data':f"An error occurred while creating the new TIFF file {err}"})

        try:
            '''
                This section opens the IMG in TIFF format, splits it into pieces to
                efficiently serve the IMG's into memory, and then provides them for 
                download.
            '''

            chunk_size = 1024 * 1024 # chunk size ; can be modified
            response = StreamingHttpResponse(handle_file_in_chnks(OutPutImg , chunk_size))
            response['Content-Disposition'] = f'attachment; filename="{NewFileName}"'
            
            return response
            
        except Exception as err:
            return JsonResponse({'status':500 , 'msg': f'Error while downlaoding File: {str(err)}'})    
    
   
    return JsonResponse({'status': 405, 'msg': 'Request method not allowed'})
   
    
    
