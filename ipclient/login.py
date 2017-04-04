#!/usr/bin/env python
# coding=utf-8

import urllib
import urllib2 
import cookielib
import re
from random import randrange
import sys


from identify  import ImageToString 

#采用utf-8编码
reload(sys)
sys.setdefaultencoding('utf-8')

# 加了头验证反而导致网页乱码,所以这里不需要headers验证
# 另外经过测试发现，获取验证码的地址，以及点击登陆按钮位置的数值需
# 要动态变化才可登陆成功，所以这里采用了random模块产生伪随机数

#headers 验证
'''
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
headers = { 'User-Agent': user_agent }
'''

#创建一个通过post方式，登陆网站的类
class PostLogin:

    def __init__( self,login_url, verify_url , image_save_path, userid, passwd ):
        
        self.login_url = login_url
        self.verify_url = verify_url
        self.image_save_path = image_save_path
        self.userid = userid
        self.passwd = passwd

    #打开一个验证码页面，获取, 验证码图片
    def get_verify_image( self  ):

        '''is very importance'''
        #生成cookie对象，   MozillaCookieJar 提供了可供读写操作的cookie,文件
        self.cookie_jar = cookielib.MozillaCookieJar()
        # 将一个保存的cookie 对象和HTTP的cookie处理器绑定
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie_jar)
        # 创建一个opener
        self.opener = urllib2.build_opener( self.cookie_support )
        # 安装opener, 此后调用urlopen的时候就会使用安装过的opener对象
        urllib2.install_opener( self.opener )

        file = urllib2.urlopen( self.verify_url  )
        verify_image_org = file.read()
        #下载图片到本地
        local_image = open( self.image_save_path, 'wb')
        try:
            local_image.write( verify_image_org )
        except IOError , e :
            print e
        finally:
            local_image.close()

        return self.image_save_path

    def make_post( self, verify ):
        userid = self.userid
        passwd = self.passwd
        post_data = urllib.urlencode( { 
            'userid': userid,
            'passwd': passwd,
            'validnum': verify,
            #post数据除,验证码要正确外，点击区域也要动态变化
            'imageField.x': str( randrange( 0, 50 ) ),
            'imageField.y': str( randrange( 0, 18 ) )
        })
        return post_data


    def login_resquest( self , post_data ):
        #构造post请求
        request = urllib2.Request(
            url = self.login_url,
            data = post_data
        )
        #返回请求结果
        return request
    
    def start_login( self ):
        verify_save =  self.get_verify_image()
        if verify_save:
            #识别验证码
            identify = ImageToString( verify_save )
            verify_code =  identify.get_string( )
        else:
            print 'get verify_image fail!'

        post_data  = self.make_post( verify_code )
        request = self.login_resquest( post_data )
        respone = urllib2.urlopen( request )
        return  respone.read().decode( 'gbk' ).encode( 'utf-8')

