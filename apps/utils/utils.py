from PIL import Image
from io import BytesIO
from django.core.files import File


def compress_image(image):
    """
    Compress image in format JPEG and specific quality 
    """
    img = Image.open(image)

    if img.format == 'JPEG':
        im_format = 'JPEG'
    elif img.format == 'PNG':
        im_format = 'PNG'
    
    im_io = BytesIO()

    #Saving the image
    img.save(im_io , format=im_format, quality=80)
    image_optimized = File(im_io, name=image.name) 

    return image_optimized


def thumbnail_image(image):
    """
    Create thumbnail of image with basewidth of 150, format JPEG and quality of 100
    """
    basewidth = 150

    img = Image.open(image) 

    if img.format == 'JPEG':
        im_format = 'JPEG'
    elif img.format == 'PNG':
        im_format = 'PNG'

    im_io = BytesIO()

    #Calculating the new size considerings its aspect ratio
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    
    #Resize/modify the image
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    
    #Saving the image
    img.save(im_io , format=im_format, quality=100)
    image_optimized = File(im_io, name=image.name)    

    return image_optimized