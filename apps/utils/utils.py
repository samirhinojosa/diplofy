from PIL import Image
from io import BytesIO
from django.core.files import File


def compress_image(image):
    """
    Compress image in format JPEG and specific quality 
    """
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io , format='JPEG', quality=80)
    image_optimized = File(im_io, name=image.name)    
    return image_optimized


def thumbnail_image(image):
    """
    Create thumbnail of image with basewidth of 150, format JPEG and quality of 100
    """
    basewidth = 150

    img = Image.open(image) #Image.open('old.jpeg').convert('RGB').save('new.jpeg')
    im_io = BytesIO()

    #Calculating the new size considerings its aspect ratio
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    
    #Resize/modify the image
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    
    #Saving the image
    img.save(im_io , format='JPEG', quality=100)
    image_optimized = File(im_io, name=image.name)    
    return image_optimized