#-*-coding:utf-8-*-
from handlers.base import BaseHandler
from utils.response_code import *
from utils.session import *
from utils.common import *
from contants import *
import json
import re
import logging
import hashlib

class UserHandler(BaseHandler):
    """"""
    def put(self):
        """响应体中的json数据已经在BaseHandler中解析"""
        mobile=self.dict.get('mobile')
        password=self.dict.get('password')
        # password2=self.dict.get('password2')
        smsCaptcha=self.dict.get('phonecode')
        if not all([mobile,password,smsCaptcha]):
           errRet={'errno':RET.PARAMERR,'errmsg':'参数不完整'}
           return self.write(json.dumps(errRet))
        if not re.match(r'1[34578]\d{9}',mobile):
           errRet={'errno':RET.PARAMERR,'errmsg':'无效手机号'}
           return self.write(json.dumps(errRet))
        try:
           smsCaptchaRedis=self.redis.get('sms_%s' % mobile)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'查询短信验证码失败'}
            return self.write(json.dumps(errRet))
        if smsCaptchaRedis is None:
            errRet={'errno':RET.NODATA,'errmsg':'短信验证码失效'}
            return self.write(json.dumps(errRet))
        if smsCaptchaRedis!=smsCaptcha:
            errRet={'errno':RET.DATAERR,'errmsg':'短信验证码校核失败'}
            return self.write(json.dumps(errRet))
        # if password!=password2:
        #     errRet={'errno':RET.DATAERR,'errmsg':'两次密码输入不一致'}
        #     return self.write(json.dumps(errRet))
        mySql='insert into ih_user_profile(up_name,up_mobile,up_passwd) values(%(name)s,%(mobile)s,%(passwd)s)'
        password=hashlib.sha256(password+SECRET_KEY).hexdigest()
        try:
            userId=self.db.execute(mySql,name=mobile,mobile=mobile,passwd=password)
            #因为mobile字段已经设置了unique属性，所以手机号重复注册的错误会被捕捉到
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'保存用户注册信息失败'}
            return self.write(json.dumps(errRet))
        try:
            mySession=Session(self)
            mySession.data['userId']=userId
            mySession.data['name']=mobile
            mySession.data['mobile']=mobile
            mySession.save()
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.SESSIONERR,'errmsg':'保存用户登陆信息失败'}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'注册成功'}
        return self.write(json.dumps(errRet))

class SessionHandler(BaseHandler):
    """对应于session操作，包括登陆/注销/查询登陆状态"""
    def put(self):
        """验证用户密码，保存session"""
        mobile=self.dict.get('mobile')
        passwd=self.dict.get('passwd')
        passwd=hashlib.sha256(passwd+SECRET_KEY).hexdigest()
        mySql='select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s'
        try:
            myRow=self.db.get(mySql,mobile=mobile)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'查询数据库失败'}
            return self.write(json.dumps(errRet))
        if not myRow:
            errRet={'errno':RET.NODATA,'errmsg':'用户未注册'}
            return self.write(json.dumps(errRet))
        if myRow['up_passwd']!=passwd:
            errRet={'errno':RET.PWDERR,'errmsg':'密码错误'}
            return self.write(json.dumps(errRet))
        try:
            mySession=Session(self)
            mySession.data['userId']=myRow['up_user_id']
            mySession.data['name']=myRow['up_name']
            mySession.data['mobile']=mobile
            mySession.save()
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.SESSIONERR,'errmsg':'保存用户登陆信息失败'}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'登陆成功'}
        return self.write(json.dumps(errRet))

    @require_login
    def delete(self):
        """删除用户session数据"""
        try:
            self.session.clear()
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.SESSIONERR,'errmsg':'注销用户登陆信息失败'}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'注销成功'}
        self.write(json.dumps(errRet))

    @require_login
    def get(self):
        """查询用户登陆状态"""
        userName=self.session.data['name']
        errRet={'errno':RET.OK,'errmsg':'用户已登陆','userName':userName}
        self.write(json.dumps(errRet))









