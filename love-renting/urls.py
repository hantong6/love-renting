#-*-coding:utf-8-*-
import os
from handlers import (base, xsrf,index,verify,passport,profile,house,order)
urls=[
    (r'^/api/index$',index.IndexHandler),
    (r'^/api/search$',index.SearchHandler),
    (r'^/api/captcha$',verify.CaptchaHandler),
    (r'^/api/sms$',verify.SmsHandler),
    (r'^/api/user$',passport.UserHandler),
    (r'^/api/session$',passport.SessionHandler),
    (r'^/api/avatar$',profile.AvatarHandler),
    (r'^/api/userinfo$',profile.UserInfoHandler),
    (r'^/api/auth$',profile.AuthHandler),
    (r'^/api/area$',house.AreaHandler),
    (r'^/api/house$',house.HouseHandler),
    (r'^/api/facility$',house.FacilityHandler),
    (r'^/api/house/detail$',house.HouseDetailHandler),
    (r'^/api/booking$',order.BookingHandler),
    (r'^/api/order$',order.OrderHandler),

    (r'^/api/xsrf_cookie$', xsrf.XSRFCookieHandler),
    (r'^/(.*)$', base.MyStaticHandler, {'path': os.path.join(os.getcwd(), 'htmls'), 'default_filename': 'index.html'}),

]