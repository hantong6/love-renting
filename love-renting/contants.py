#-*-coding:utf-8-*-

#调用xsrf_cookie请求接口的验证口令
XSRF_COMMAND='hantong6'

#验证码过期时间s
CAPTCHA_EXPIRES=60

#短信验证码过期时间
SMS_EXPIRES=60

#session过期时间
SESSION_EXPIRES=86400

#areas_info过期时间
AREA_EXPIRES=86400

#index_image过期时间
INDEX_EXPIRES=86400

#搜索页每页展示房远数量
SEARCH_PAGE_CAPACITY=3

#搜索页缓存页数
SEARCH_REDIS_PAGE=10

#搜索页缓存页数过期时间
SEARCH_PAGE_EXPIRES=86400

#密码盐值
SECRET_KEY='hantong6'

#七牛路径
QIUNIU_PATH='http://otl2g1dz5.bkt.clouddn.com/'