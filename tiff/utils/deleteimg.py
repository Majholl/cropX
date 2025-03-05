from django.conf import settings
import os , time , shutil
from datetime import datetime


def crontab_for_deleteIm_path():
    try:
        '''
            This file is for cronjob in remove unused directory for 30 minutes
            In cronjob : 
                -- */10 * * * * python /ROOT_TO_YOUR_PROJECT/manage.py removeImgdir
        '''
        
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

