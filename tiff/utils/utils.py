from PIL import Image , ImageSequence
import os 


#save image in the given path
def write_in_storage(TIFF_path , IMAGE_form):
    '''
        Open the Tiff IMG and write it on the disk
    '''
    with open(TIFF_path , 'wb') as f:
        for chnk in IMAGE_form.chunks(): # chunks for better memory handling
            f.write(chnk)
    
    

def load_saved_images(TIFF_path , IMAGE_form , USER_mediadir , USER_sessionid , RESULT_lists):
    try:
        '''
            Extracting IMG's inside tiff file and saving it on the disk
        '''
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
    





def handle_file_in_chnks(FILE_path, chnk_size):
    '''
        Open finally output tiff file in chunkc for download 
    '''
    with open(FILE_path , 'rb') as file:
        while chnk := file.read(chnk_size):
            yield chnk