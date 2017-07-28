#-*-coding:utf-8-*-
from handlers import base
from contants import XSRF_COMMAND

class XSRFCookieHandler(base.BaseHandler):
    """前端获取xsrf的接口"""
    def get(self):
        myXsrf=self.get_argument('xsrf')
        if myXsrf==XSRF_COMMAND:
            """验证xsrf请求是否合法"""
            self.xsrf_token
            self.write('OK')
        else:
            self.send_error(403)