from rest_framework.decorators import api_view 
from rest_framework.request import Request
from rest_framework.response import Response
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework import status
import string , random , os
from os import path
from PIL import Image, ImageSequence



@api_view(['POST'])
def get_file(request:Request) -> Response:
    """
        - Upload endpoint and extacting Images from tiff file and save them.
        - Set cookie for identifier of the user
    """
    data = request.data 
    userid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    try:
        if 'file' not in data or len(data['file']) == 0 :
            return Response({'msg':'Fields are empty.', 'field-name':'file', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'file' in data:
            if path.splitext(data['file'].name)[-1] not in ['.tiff', '.TIFF', '.tif', '.TIF']:
                return Response({'msg':'File type not supported.', 'supported-type':'.tiff, .TIFF, .tif, .TIF', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        make_directory = path.join(settings.MEDIA_ROOT, userid)
        os.makedirs(make_directory, exist_ok=True)
        file_dir = path.join(make_directory, data['file'].name)
        
        
        with open(file_dir, 'wb') as f:
            for chunk in data['file'].chunks():
                f.write(chunk)
        f.close()
        
        images = []
        with Image.open(file_dir) as img :
            for ind, page in enumerate(ImageSequence.Iterator(img), 1):
                image_name = f'{os.path.splitext(data["file"].name)[0]}_page_{ind}.png'
                image_path = os.path.join(make_directory, image_name)
                page.save(image_path, 'PNG',)
                page.save(image_path, 'WebP',)
                images.append(f'/media/{userid}/{image_name}')
        resp = Response({'msg':'Request successfully.', 'status':201, 'id':userid, 'data':images}, status=status.HTTP_201_CREATED)
        Response.set_cookie(resp, 'id', userid, max_age=3600, secure=True, samesite='None', httponly=True)
        return resp
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    




@api_view(['POST'])
def rotate_img(request:Request) -> Response:
    """
        - Rotate images into angles based on the list recieving and save them.
    """
    data = request.data 
    cookie = request.COOKIES.get('id')
    try:
        if not cookie:
            return Response({'msg':'Missing ID cookie.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        keys = data.keys()
        for key, values in data.items():    
            relative_path = key.replace('/media/', '')
            path_img = os.path.join(settings.MEDIA_ROOT, relative_path)
            image = Image.open(path_img)
            rotate = image.rotate(-int(values), expand=True, fillcolor=(255,255,255))
            rotate.save(path_img)

        resp = Response({'msg':'Rotation successfully completed.', 'status':200, 'data':keys}, status=status.HTTP_200_OK)
        return resp
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['POST'])
def delete_img(request:Request) -> Response:
    """
        - Delete images based on the list recieving. 
    """
    data = request.data 
    cookie = request.COOKIES.get('id')
    try:
        if not cookie:
            return Response({'msg':'Missing ID cookie.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        keys = data.keys()
        for key in data:    
            relative_path = key.replace('/media/', '')
            path_img = os.path.join(settings.MEDIA_ROOT, relative_path)
            os.remove(path_img)
            
        resp = Response({'msg':'Deleting successfully completed.', 'status':200, 'data':keys}, status=status.HTTP_200_OK)
        return resp
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    





@api_view(['POST'])
def reorder_img(request:Request) -> Response:
    """
        - Reorder images based on the list recieving and also provide downlaodable link into response. 
    """
    data = request.data 
    cookie = request.COOKIES.get('id')
    try:
        if not cookie:
            return Response({'msg':'Missing ID cookie.', 'status':400}, status=status.HTTP_400_BAD_REQUEST)
        
        img = []
        
        for i in data['file']:
            relative_path = i.replace('/media/', '')
            path_img = os.path.join(settings.MEDIA_ROOT, relative_path)
            img.append(Image.open(path_img))
        
        
        new_file =  f'editedimg_{cookie}.tiff'
        output_dir = os.path.join(settings.MEDIA_ROOT, cookie, new_file)
        img[0].save(output_dir, save_all=True, append_images=img[1:], format="TIFF", compression='tiff_adobe_deflate')
        
        download = request.build_absolute_uri(f'/api/download/{cookie}/{new_file}')
        resp = Response({'msg':'Reordering successfully completed.', 'status':200, 'data':download}, status=status.HTTP_200_OK)
        return resp
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
    
    
    
def download_file(request, id, filename):
    """
        - Prepare requested file based on the name.
    """
    file_path = path.join(settings.MEDIA_ROOT, id, filename)
    if path.exists(file_path):
        resp = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        resp.delete_cookie('id')
        return resp
    else:
        return Http404('file not found.')