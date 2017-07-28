#-*-coding:utf-8-*-
from base import BaseHandler
from utils.captcha.captcha import captcha
from utils.response_code import *
from libs.yuntongxun.sendsms import SendSms
from contants import *
import random
import logging
import json
import re

class CaptchaHandler(BaseHandler):
    """图片验证码处理"""
    def get(self):
        captchaId=self.get_argument('id')
        name,text,myCaptcha=captcha.generate_captcha()
        try:
            # self.redis.set('captcha_%d' % captchaId,text)
            # self.redis.expire('captcha_%d' % captchaId,CAPTCHA_EXPIRES)
            self.redis.setex('captcha_%s' % captchaId,CAPTCHA_EXPIRES,text)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'验证码生成异常',}
            self.write(json.dumps(errRet))
        else:
            self.write(myCaptcha)
            self.set_header('Content-Type','image/jpg')

class SmsHandler(BaseHandler):
    """短信验证码处理"""
    def get(self):
        #先校对验证码
        mobile=self.get_argument('mobile')
        captchaText=self.get_argument('text')
        captchaId=self.get_argument('id')
        if not re.match(r'1[34578]\d{9}',mobile):
            errRet={'errno':RET.PARAMERR,'errmsg':'无效手机号'}
            return self.write(json.dumps(errRet))
        try:
             captchaRedis=self.redis.get('captcha_%s' % captchaId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DATAERR,'errmsg':'验证码读取异常'}
            return self.write(json.dumps(errRet))
        if captchaRedis is None:
            errRet={'errno':RET.NODATA,'errmsg':'验证码失效'}
            return self.write(json.dumps(errRet))
        if captchaText.lower()!=captchaRedis.lower():
            errRet={'errno':RET.DATAERR,'errmsg':'验证码校对失败'}
            return self.write(json.dumps(errRet))
        #再验证是否手机号重复注册
        mySql='select count(*) as counts from ih_user_profile where up_mobile=%s'
        try:
            myRow=self.db.get(mySql,mobile)
        except Exception as myError:
            logging.error(myError)
        else:
            if myRow['counts']:
                errRet={'errno':RET.DATAEXIST,'errmsg':'手机号已经注册'}
                return self.write(json.dumps(errRet))
        #最后发送短信验证码
        smsCaptcha='%06d' % random.randint(0,999999)
        try:
            self.redis.setex('sms_%s' % mobile,SMS_EXPIRES,smsCaptcha)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'短信验证码生成异常'}
            return self.write(json.dumps(errRet))
        try:
            mySender=SendSms()
            mySender.sendTemplateSms(mobile,[smsCaptcha,str(SMS_EXPIRES/60)],1)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.THIRDERR,'errmsg':'短信发送失败'}
            self.write(json.dumps(errRet))
        else:
            errRet={'errno':RET.OK,'errmsg':'短信发送成功'}
            self.write(json.dumps(errRet))
