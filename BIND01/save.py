import os
import sys
from PIL import Image
import shutil
#input2='/home/jack/Desktop/deep-dream-generator/notebooks/bugs/butterflies/000163.jpg'
input1='GREEN.jpg'
#input1='/home/jack/Desktop/imagebot/colorful/20170824124329.jpg'
input2='flower.jpg'
shutil.copy2(input1, 'instagram/') # complete target filename given
shutil.copy2(input2, 'instagram/')# target filename is /dst/dir/file.ext

aa = Image.open(input1).convert("RGB")
#bb = Image.open("/home/jack/Documents/GG.jpg").convert("RGB")
bb = Image.open(input2).convert("RGB")
xx=aa.resize((640,640), Image.NEAREST)
yy=bb.resize((640,640), Image.NEAREST)
xx.save("junk/aa.png")
yy.save("junk/bb.png")
src = Image.open('junk/aa.png').convert('RGB')
dst = Image.open('junk/bb.png').convert('RGB')
src.save("junk/aa.png")
dst.save("junk/bb.png")