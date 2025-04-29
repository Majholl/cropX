from rest_framework.decorators import api_view 
from rest_framework.request import Request
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
import string , random , os
from os import path
from PIL import Image, ImageSequence
from datetime import timedelta





@api_view(['POST'])
def get_file(request:Request) -> Response:
    
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
                page.save(image_path, 'PNG')
                images.append(f'/media/{userid}/{image_name}')
        resp = Response({'msg':'Request successfully.', 'status':201, 'id':userid, 'data':images}, status=status.HTTP_201_CREATED)
        Response.set_cookie(resp, 'id', userid, max_age=3600)
        return resp
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    










@api_view(['POST'])
def rotate_img(request:Request) -> Response:
    
    data = request.data 
    cookie = request.COOKIES['id']
    try:
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
    
    data = request.data 
    cookie = request.COOKIES['id']
    try:
        keys = data.keys()
        for key in data:    
            relative_path = key.replace('/media/', '')
            path_img = os.path.join(settings.MEDIA_ROOT, relative_path)
            os.remove(path_img)
            
        resp = Response({'msg':'Deleting successfully completed.', 'status':200, 'data':keys}, status=status.HTTP_200_OK)
        return resp
    
    except Exception as err:
        return Response({'msg':'Internal server error.', 'status':500, 'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
