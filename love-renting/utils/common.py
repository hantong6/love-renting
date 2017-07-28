#-*-coding:utf-8-*-
from utils.response_code import *
import json
import functools

def require_login(fun):
    #此处装饰器还原被装饰函数属性，包括说明文档等
    @functools.wraps(fun)
    def wrapper(handler,*args,**kwargs):
        if not handler.get_current_user():
            errRet={'errno':RET.SESSIONERR,'errmsg':'用户未登陆'}
            handler.write(json.dumps(errRet))
        else:
            fun(handler,*args,**kwargs)
    return wrapper