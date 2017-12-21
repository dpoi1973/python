from wand.color import Color
from wand.image import Image as imagss
from wand.image import COMPOSITE_OPERATORS
from wand.drawing import Drawing
from wand.display import display
from PIL import Image as imagg
import numpy as np
import datetime
import matplotlib.pyplot as plt
import cv2
import os, os.path, sys
import glob
import re 
from reportlab.lib.pagesizes import A4, landscape  
from reportlab.platypus import SimpleDocTemplate, flowables, Paragraph, Image, PageBreak  
from reportlab.platypus import PageTemplate, Frame  
from PyPDF2 import PdfFileReader


def pdf2jpg(source_file, target_file):
    RESOLUTION = 250
    inpdf = PdfFileReader(open(source_file, 'rb'))
    try:
        with imagss(filename=source_file, resolution=(RESOLUTION,RESOLUTION)) as img:
            # print (img.size)
            img.background_color = Color('white')
            img.alpha_channel = False
            img.format = 'png'
            if inpdf.getNumPages() == 1:
                img.save(filename = target_file.split('.')[0]+"-0.png")
            else:
                img.save(filename = target_file)
    except Exception as e:
        print(e)
        return False

    return inpdf.getNumPages()

# pdf2jpg('images/79651.pdf','test.png')
# random add noise by

def randomPixel1(src,repeat,chanceRatio):
    # print(src.shape)
    # repeat = 2
    # chanceRatio= 16 
    
    ydiv = [1,0,0,0,0,0,0,0,0,-1]

    (rows,cols) = src.shape
    radarray = np.random.rand(rows,cols)
    for (rowid, row) in enumerate(src):
       # if rowid == 0: break
        for (cid,c) in enumerate(row):
           # if cid ==0 or cid  == cols-1: break
            for x in [0,repeat]:
                if x >0 and cid >0 and cid < (cols - 1) :
                    ramdomchance = int(radarray[rowid,cid]* 100) #np.random.random_integers(0,100)
                   # print ramdomchance
                    #ramdomchance = np.random.random_integers(0,100)
                    if ramdomchance < chanceRatio:
                        rand2 =     ramdomchance  % 10
                        vx = rowid -1
                        vy = ydiv[rand2]

                        src[rowid,cid] =src [vx,vy]
                        src[rowid,cid] = 254

def randomPixel2(wizard,rose,oupng):
    ret = True
    w = wizard.clone()
    r = rose.clone()
    with Drawing() as draw:
        draw.composite(operator='subtract', left=400, top=1500,
                    width=600, height=600, image=r)
        draw(w)
        w.save(filename=oupng)
        return ret


# trans png to tiff

def randomPixel3(inimg,outimg):
    im = imagg.open(inimg) #'images/79651-1.png'
    # im.show()
    ret = True
    imarray = np.array(im)
    im.info

    imagenew = im.convert('1')

    arrtif = np.array(imagenew)

    imagenew.save(outimg,compression='group4')

    # print (imarray.shape)
    return ret



def create_pdf(fname, arr, path):   
    filename =  path +fname.split('/')[6]+".pdf"
    width,height = landscape(A4) 
    print("width = %d, height = %d\n" % (width, height))  
    doc = SimpleDocTemplate(filename, pagesize=(height, width))  
    frame1 = Frame(0, 0, height, width, 0, 0, 0, 0, id="normal1")  
    doc.addPageTemplates([PageTemplate(id="Later", frames=frame1)])  
    Story=[]
    for pic in arr:
        # with imagss(filename=pic) as original:
        #      with original.convert('pdf') as converted:  
        #          Story.append(converted) 
        im = Image(pic, height, width)
        Story.append(im)  
        Story.append(PageBreak())  
        print (pic)  
    doc.build(Story)  
    print ("%s created" % filename) 
    return filename


def imgconver(fname, arr, path):
    # arr = ['images/79651-0.tif','images/79651-1.tif']
    # oo = []
    filenames =  path + fname.split('/')[6]+".pdf"
    for pp in arr:
        with imagss(filename=pp) as original:
            with original.convert('pdf') as converted:
                # operations to a jpeg image...
                # oo.append(converted)
                converted.save(filename=filenames)
                return filenames
# test()
# arr = ['images/79651-0.tif','images/12.tif']
# create_pdf("/home/wanli/src/pdftest/images/test.png" ,arr,"/home/wanli/src/pdftest/path/")
def changgepdf(source_file):
    target_file = source_file.split('.')[0]+".png"
    # r"/home/wanli/src/pdftest/images/79651.png"
    ret = pdf2jpg(source_file, target_file)
    tt = []
    for i in range(0,ret):
        print(i)
        pngfile = target_file.split('.')[0]+"-"+str(i)+".png"
        img = cv2.imread(pngfile,0)
        randomPixel1(img,2,16)
        # cv2.waitKey()
        cv2.imwrite(pngfile, img)
        cv2.destroyAllWindows()
        print(pngfile)
        rose = imagss(filename='./images/1-200.png')
        wizard = imagss(filename=pngfile)
        outpng = randomPixel2(wizard,rose,pngfile)
        ooo = pngfile.split('.')[0]+'.tif'
        randomPixel3(pngfile,ooo)
        tt.append(ooo)


    path = "/home/wanli/src/pdftest/path/"  
    print(tt)
    # return create_pdf(target_file.split('.')[0], tt, path)
    return imgconver(target_file.split('.')[0],tt,path)