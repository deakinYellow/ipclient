#!/usr/bin/env python
# coding=utf-8

import urllib2
import urllib
import re
import cookielib
from random import randrange
import sys
import time

from login  import PostLogin 
from info import PageInfo

#登录主页面地址
LOGIN_URL = 'http://172.16.1.1/ipmanager/index0.jsp' 
#验证码获取地址,末尾必须时6个随机数字字符
VRIFY_CODE_URL = 'http://172.16.1.1/ipmanager/servlet/randomnum?t=1460018' +\
        str( randrange(100000, 999999 ) )
#验证码存放路径
VRIFY_IMAGE_SAVE_PATH = './.verifyImage.gif'


def user_login( userid, passwd ):
    
    log = PostLogin( LOGIN_URL, VRIFY_CODE_URL, VRIFY_IMAGE_SAVE_PATH,
        userid, passwd
        )
    page =  log.start_login( )
    #生成一个页面处理对象
    log_page = PageInfo( page )
    log_result = log_page.get_login_result( ) 
    print '---------------------------------------------------------'

    if log_result['result'] == True :
        #获取账户余额
        user_balance =  log_page.get_user_info()
        print 'balance is : ', user_balance
        return 100
    
    #user name or passwd error
    elif log_result['code'] == 101 :
        print log_result['message'],'please try again'
        return 101
    #verify error, auto try next login
    elif log_result['code'] == 102 :
        print 'verify code error auto try next login'
        return 102




if __name__ == '__main__':
    print '-------------------------------------------------------------'
    print '|             guet ipclient for linux                       |'
    print '|             version: 0.01                                 |'
    print '|             email: deakin_dj@163.com                      |'
    print '-------------------------------------------------------------'
    new_login = True
    try_time = 0
    login_result = None 
    while True :
        if new_login and login_result != 102 :
            userid = raw_input( 'user id:')
            passwd = raw_input( 'password:')

        if try_time <= 5 :
            login_result = user_login( userid, passwd )
            if login_result == 100 :
                if new_login :
                    new_login = False
                    try_time = 0
                    print 'login successful, maybe you can surf the internet now.'
                    print 'the programe will auto refresh every 5 minutes.'

                time.sleep( 300 )
            elif login_result == 102 :
                try_time = try_time + 1

        else :
            print 'error: verify code can not identify.'
            exit( 0 )



