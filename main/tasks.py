from django.conf import settings
from os import path
import os
import shutil
from datetime import datetime



def delete_useless_files():
    try:        
        BaseDir = settings.MEDIA_ROOT
        paths = [os.path.join(BaseDir , i) for i in os.listdir(BaseDir)]
        PathCount , FileCount = 0 , 0 
        
        now_timestamp = datetime.now()
        for i in paths:
            cal_time = (now_timestamp - datetime.fromtimestamp(os.path.getmtime(i)))
            if cal_time.seconds > 1800: # 1800 -> 30 min
                if os.path.isdir(i):
                    shutil.rmtree(i)
                    PathCount +=1
                elif os.path.isfile(i):
                    os.remove(i)
                    FileCount +=1

        print(f'{PathCount} paths and {FileCount} files removed due to passing one hour')
    except Exception as err:
        print(f'Error while removing unsued Directory for one hour')
     
     
        
