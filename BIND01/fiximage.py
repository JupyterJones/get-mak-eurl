#!/bin/bash/python
# Takes an image and based on the smalles side crops from the center 
# then resizes 640x640
# use example:
# import fiximage
# fiximage.fix('MONA.jpg', '640MONA.jpg')

def fix(filein,fileout):
    from PIL import Image
    img = Image.open(filein)
    width = img.size[0]
    height = img.size[1]
    imin1 = min(img.size)
    img3 = img.crop(
        (
            width - imin1,
            height - imin1,
            width,
            height
        )
    )
    im3 = img3.resize((640,640), Image.NEAREST)
    im3.save(fileout)
    return im3