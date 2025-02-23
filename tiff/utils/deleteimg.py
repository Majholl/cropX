from django.conf import settings
import os , time , shutil
from background_task import background


def crontab_for_deleteIm_path():
    try:
        '''
            This file is for cronjob in remove unused directory for one hour 
            In cronjob : 
                -- */10 * * * * python /ROOT_TO_YOUR_PROJECT/manage.py removeImgdir
        '''
        BaseDir = settings.MEDIA_ROOT
        paths = [os.path.join(BaseDir , i) for i in os.listdir(BaseDir)]
        PathCount = 0 
        FileCount = 0
        for i in paths:
            if time.time() - os.path.getatime(i) > 3600:
                if os.path.isdir(i):
                    shutil.rmtree(i)
                    PathCount +=1
                elif os.path.isfile(i):
                    os.remove(i)
                    FileCount +=1

        print(f'{PathCount} paths and {FileCount} files removed due to passing one hour')
    except Exception as err:
        print(f'Error while removing unsued Directory for one hour')

