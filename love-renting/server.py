#-*-coding:utf-8-*-
from tornado import (options,httpserver,ioloop)
from tornado.web import Application
import torndb
import redis
import config
import urls

class MyApplication(Application):
    """继承Application，添加数据库连接"""
    def __init__(self,*args,**kwargs):
        super(MyApplication,self).__init__(*args,**kwargs)
        self.db=torndb.Connection(**config.mysql_options)
        self.redis=redis.StrictRedis(**config.redis_options)

def main():
    """"""
    options.options.log_file_prefix=config.log_files_path
    options.options.logging=config.log_lever
    options.options.log_file_max_size=config.log_file_max_size
    options.options.log_file_num_backups=config.log_file_num_backups
    options.define('port',default=8000,type=int,help='绑定服务器端口')
    options.parse_command_line()

    myApp=MyApplication(urls.urls,**config.settings)
    myServer=httpserver.HTTPServer(myApp)
    myServer.bind(options.options.port,'192.168.119.20')
    myServer.start()

    ioloop.IOLoop.current().start()

if __name__=='__main__':
    main()