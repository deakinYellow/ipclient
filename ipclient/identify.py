#!/usr/bin/env python
# coding=utf-8

import sys
import Image, ImageEnhance ,ImageFilter
from  pytesser.pytesser import *

class ImageToString:

    def __init__( self, image ):
        self.image = image

    def get_string( self ):
        #二值化
        threshold = 110 
        table = []
        for  i in range( 256 ):
            if i < threshold:
                table.append( 0 )
            else:
                table.append( 1 )

        im = Image.open( self.image )

        #降低灰度
        imgry = im.convert('L')
        #二值化
        out = imgry.point( table, '1' )
        #identify ,
        text = image_to_string( out )
    
        # 去掉空格,如果识别成大写则全部改为小写
        # 因为要登录网站的验证码均为小写字母
        text = text.strip().lower()
    
        if text.__len__() == 4:
            return text 
        else:
            print 'identify error!!!'
            return None  




