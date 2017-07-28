#-*-coding:utf-8-*-
from contants import *
import uuid
import json
import logging

class Session(object):
    """session代理类"""
    def __init__(self,handler):
        self.handler=handler
        sid=self.handler.get_secure_cookie('session_id')
        if sid is None:
            self.sid=uuid.uuid4().get_hex()
            self.data={}
        else:
            self.sid=sid
            try:
                myJson=self.handler.redis.get('session_%s' % self.sid)
            except Exception as myError:
                logging.error(myError)
                raise myError
            if myJson is None:
                raise Exception('session失效')
            self.data=json.loads(myJson)

    def save(self):
        myJson=json.dumps(self.data)
        try:
            self.handler.redis.setex('session_%s' % self.sid,SESSION_EXPIRES,myJson)
        except Exception as myError:
            logging.error(myError)
            raise myError
        else:
            self.handler.set_secure_cookie('session_id',self.sid)

    def clear(self):
        try:
            self.handler.redis.delete('session_%s' % self.sid)
        except Exception as myError:
            logging.error(myError)
        self.handler.clear_cookie('session_id')

if __name__=='__main__':
    mySession=Session()
    mySession.data={}
