#!/home/jack/anaconda2/bin
from PIL import Image
import sys
sys.argv
def resize640(image, output):
    Bp=Image.open(image)
    width, height = Bp.size
    w1=int((width-height)/2)
    w2 = int(width-w1)
    h1=height-height
    h2=height
    Cc=Bp.crop((w1,h1,w2,h2))
    result = Cc.resize((640,640), Image.NEAREST)
    result.save(output)
if __name__ == '__main__':
    image = sys.arg[1:]
    output = sys.arg[2:]
    resize640(image, output)        