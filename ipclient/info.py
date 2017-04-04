#!/usr/bin/env python
# coding=utf-8


import re

'''
处理登陆后返回的信息，
1.返回登录结果
2.登录成功，账户余额，刷新时间等
'''
class PageInfo:

    def __init__( self, page ):
        self.page = page

    def __get_info( self, obj_re ):
        obj_pattern = re.compile( obj_re, re.S )
        info = re.search( obj_pattern, self.page )
        return info


    def get_login_result( self ):
        exception_re = '<script>alert(.*?);</script>'
        result = self.__get_info( exception_re )
        #print 'the login result：' , result
        log_result = {'result': None , 'code': None , 'message': None }

        if result == None :
            log_result['result'] = True
            log_result['message'] = 'login successful'

        else :
            log_result['result'] = False
            result_info = result.group(1)
            if result_info == '("用户名或密码错误")':
                log_result['code'] = 101
                log_result['message'] = 'user name or passwd error'
            elif result_info == '("验证码错误")':
                log_result['code'] = 102
                log_result['message'] = 'verify code error'

        return log_result


    def get_user_info( self ):
        
        balance_re = '剩余金额：(.*?)</td>'
        balance = self.__get_info( balance_re )

        if  balance != None:
             return  balance.group(1)
        else:
             return None

