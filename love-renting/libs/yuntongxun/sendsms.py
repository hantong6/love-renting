#coding=gbk
#coding=utf-8
#-*- coding: UTF-8 -*-
from CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= '8aaf07085d106c7f015d636b09632432'
#���ʺ�Token
accountToken= 'ef93b2c8b69f479dad5132f1da52ad49'
#Ӧ��Id
appId='8aaf07085d106c7f015d636b09ab2437'
#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com'
#����˿� 
serverPort='8883'
#REST�汾��
softVersion='2013-12-26'

# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

class SendSms(object):
    """"""
    def __new__(cls,*args,**kwargs):
        #��ʼ��REST SDK
        if hasattr(cls,'_SendSms__single'):
            return cls.__single
        else:
            cls.__single=super(SendSms,cls).__new__(cls,*args,**kwargs)
            cls.__single.rest = REST(serverIP,serverPort,softVersion)
            cls.__single.rest.setAccount(accountSid,accountToken)
            cls.__single.rest.setAppId(appId)
            return cls.__single

    def sendTemplateSms(self,to,datas,tempId):
        #���Ͷ��Ź��ܺ���
        result = self.rest.sendTemplateSMS(to,datas,tempId)
        if result.get('statusCode')!='000000':
            raise Exception(u'���Ͷ����쳣��%s' % result.get('statusMsg'))
        # for k,v in result.iteritems():
        #     if k=='templateSMS' :
        #         for k,s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)

if __name__=='__main__':
    """���ܲ���"""
    mySend=SendSms()
    mySend.sendTemplateSms('18301782093',['1234','3'],1)
