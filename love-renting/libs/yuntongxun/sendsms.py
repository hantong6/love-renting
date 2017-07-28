#coding=gbk
#coding=utf-8
#-*- coding: UTF-8 -*-
from CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8aaf07085d106c7f015d636b09632432'
#主帐号Token
accountToken= 'ef93b2c8b69f479dad5132f1da52ad49'
#应用Id
appId='8aaf07085d106c7f015d636b09ab2437'
#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'
#请求端口 
serverPort='8883'
#REST版本号
softVersion='2013-12-26'

# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

class SendSms(object):
    """"""
    def __new__(cls,*args,**kwargs):
        #初始化REST SDK
        if hasattr(cls,'_SendSms__single'):
            return cls.__single
        else:
            cls.__single=super(SendSms,cls).__new__(cls,*args,**kwargs)
            cls.__single.rest = REST(serverIP,serverPort,softVersion)
            cls.__single.rest.setAccount(accountSid,accountToken)
            cls.__single.rest.setAppId(appId)
            return cls.__single

    def sendTemplateSms(self,to,datas,tempId):
        #发送短信功能函数
        result = self.rest.sendTemplateSMS(to,datas,tempId)
        if result.get('statusCode')!='000000':
            raise Exception(u'发送短信异常：%s' % result.get('statusMsg'))
        # for k,v in result.iteritems():
        #     if k=='templateSMS' :
        #         for k,s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)

if __name__=='__main__':
    """功能测试"""
    mySend=SendSms()
    mySend.sendTemplateSms('18301782093',['1234','3'],1)
