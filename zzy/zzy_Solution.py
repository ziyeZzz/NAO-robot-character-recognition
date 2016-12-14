# -*- coding: utf-8 -*-
from naoqi import ALProxy
import sys
import numpy as np
from PIL import Image
from pylab import *
import cv2
import cv2.cv as cv
import tesseract
import urllib2, re, HTMLParser
import os

#########----***---GET---Picture---Part----***---#########
'''resolution = 2  #VGA
colorSpace = 11 #RGB
camProxy = ALProxy("ALVideoDevice","192.168.1.145", 9559)
videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

# The image returned and save it as a PNG using ImageDraw
# package.
# Get the image size and pixel array.
naoImage = camProxy.getImageRemote(videoClient)
camProxy.unsubscribe(videoClient)

tts = ALProxy("ALTextToSpeech", "192.168.1.145", 9559)
print "finished"
tts.say("\\rspd=100\\"+"OK! I already remembered it!",'English')

imageWidth = naoImage[0]
imageHeight = naoImage[1]
array = naoImage[6]
# Create a PIL Image from our pixel array.
im = Image.frombytes("RGB", (imageWidth, imageHeight), 
array)
# Save the image.
im.save("c1.png", "PNG")'''

def ocr_sxx(filename):
        #####Image preprocess#####
        im = cv2.imread(filename)

        #convert to grayscale and apply Gaussian filtering 
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('result1',im_gray)
        # Threshold the image
        ret,im_th = cv2.threshold(im_gray, 70, 255, cv2.THRESH_BINARY)
        #cv2.imshow('result2',im_th)
        #remove noise
        im_th = cv2.medianBlur(im_th,3)
        #check result
        #cv2.imshow('result',im_th)
        #save the image in local computer
        cv2.imwrite('result.png',im_th)
        cv2.waitKey(0)          # Waits forever for user to press any key
        cv2.destroyAllWindows()

        #########----OCR Part----########
        image=cv.LoadImage("result.png", cv.CV_LOAD_IMAGE_GRAYSCALE)
        directory= "tessdata/"
        ########choose language############
        InputLan = "eng"
        api = tesseract.TessBaseAPI()
        fileName = InputLan+'.traineddata'
        fullPath = directory+fileName
           
        api.Init(".",InputLan,tesseract.OEM_DEFAULT)                                       
        #api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
        api.SetPageSegMode(tesseract.PSM_AUTO)
        tesseract.SetCvImage(image,api)
        text=api.GetUTF8Text()

        conf=api.MeanTextConf()
        timage=None
        print len(text)
        #text = text.decode('utf-8') #from str to unicode
        print text.decode('utf-8')
        #print conf
        ########delete /n ############
        line=text.replace('\n',' ')
        #line = line.decode('utf-8')
        print line.decode('utf-8')               
       

############main############
file_name = "c1.png"
ocr_sxx(file_name)
