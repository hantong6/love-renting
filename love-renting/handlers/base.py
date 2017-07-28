#-*-coding:utf-8-*-
from tornado.web import (RequestHandler,StaticFileHandler)
from utils.session import *
import json

class BaseHandler(RequestHandler):
    """自定义请求基类，实现通用方法"""
    def prepare(self):
        """预处理方法，对用户发送过来的json数据解析"""
        if self.request.headers.get('Content-Type','').startswith('application/json'):
            myJson=self.request.body
            self.dict=json.loads(myJson)
        else:
            self.dict={}

    def set_default_headers(self):
        """设置默认的响应头信息"""
        self.set_header('Content-Type','application/json;charset=utf-8')

    def get_current_user(self):
        """配合require_login装饰器使用"""
        self.session=Session(self)
        return self.session.data

    @property
    def db(self):
        """简化数据库调用操作"""
        return self.application.db

    @property
    def redis(self):
        """简化数据库调用操作"""
        return self.application.redis

class MyStaticHandler(StaticFileHandler):
    """自定义静态文件处理类，用户第一次请求即设置xsrf"""
    def __init__(self,*args,**kwargs):
        super(MyStaticHandler,self).__init__(*args,**kwargs)
        self.xsrf_token