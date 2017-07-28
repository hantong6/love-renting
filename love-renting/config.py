#-*-coding:utf-8-*-
import os
import base64
import uuid

settings=dict(
    debug = True,
    static_path = os.path.join(os.getcwd(), 'static'),
    xsrf_cookies = True,
    cookie_secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
)

mysql_options=dict(
    host='127.0.0.1',
    database='ihome',
    user='python',
    password='a123456a',
)

redis_options=dict(
    host='127.0.0.1',
    port=6379,
)

log_files_path='./logs/log'
log_lever='debug'
log_file_max_size=65536
log_file_num_backups=1