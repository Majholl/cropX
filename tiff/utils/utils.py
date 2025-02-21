from PIL import Image , ImageSequence
import os

def write_in_storage(TIFF_path , IMAGE_form):
    with open(TIFF_path , 'wb') as f:
        for chnk in IMAGE_form.chunks():
            f.write(chnk)
    

def load_saved_images(TIFF_path , IMAGE_form , USER_mediadir , USER_sessionid , RESULT_lists):
    try:
        ImageURLpath = []
        with Image.open(TIFF_path) as opImg:
            for ind , page in enumerate(ImageSequence.Iterator(opImg) , 1):
                ImageFileName = f'{os.path.splitext(IMAGE_form.name)[0]}_page_{ind}.png'
                ImagePath = os.path.join(USER_mediadir , ImageFileName)
                page.save(ImagePath , 'PNG')
                ImageURLpath.append(f"/media/{USER_sessionid}/{ImageFileName}")
        RESULT_lists.extend(ImageURLpath)
    except Exception as err:
        return f'error while load images {err}'        
    

def StreamDownloadFile(FILE_path):
    with open(FILE_path , 'rb') as f:
        while chnk := f.read(8192):
            yield chnk