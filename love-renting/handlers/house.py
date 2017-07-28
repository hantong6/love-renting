#-*-coding:utf-8-*-
from handlers.base import BaseHandler
from utils.response_code import *
from libs.qiniu.upload import up_load
from utils.common import *
from utils import session
from contants import *
from dateutil import tz
from dateutil.tz import tzlocal
from datetime import datetime
import logging
import json

class AreaHandler(BaseHandler):
    """城区信息接口"""
    def get(self):
        #首先查询redis
        try:
            myRows=self.redis.get('areas')
        except Exception as myError:
            logging.error(myError)
            myRows=None
        if myRows:
            # errRet={'errno':RET.OK,'errmsg':'查询城区成功','data':json.loads(myRows)}
            # return self.write(json.dumps(errRet))
            # 从redis中获取的myRows是json格式，需要先解析，再和errno，errmsg一起打包成json格式，这里用直接拼接成json字符串的方式优化
            myJson='{"errno":"0","errmsg":"查询城区成功","data":%s}' % myRows
            return self.write(myJson)
        #若redis中无缓存数据
        mySql='select ai_area_id as aid,ai_name as aname from ih_area_info'
        try:
            myRows=self.db.query(mySql)
        except Exception as  myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'查询城区失败'}
            self.write(json.dumps(errRet))
        else:
            #将数据缓存至redis中
            try:
                self.redis.setex('areas',AREA_EXPIRES,json.dumps(myRows))
            except Exception as myError:
                logging.error(myError)
            errRet={'errno':RET.OK,'errmsg':'查询城区成功','data':myRows}
            self.write(json.dumps(errRet))

class HouseHandler(BaseHandler):
    """获取/设置房源的接口"""
    @require_login
    def get(self):
        userId=self.session.data['userId']
        mySql='select a.hi_house_id as house_id,a.hi_title as title,b.ai_name as address,a.hi_price as price,a.hi_ctime as ctime,a.hi_index_image_url as image_url from ih_house_info as a inner join ih_area_info as b on a.hi_area_id=b.ai_area_id where a.hi_user_id=%(user_id)s'
        try:
            myRows=self.db.query(mySql,user_id=userId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'查询房源失败'}
            return self.write(json.dumps(errRet))
        fromZone = tz.gettz('UTC')
        toZone = tz.gettz('CST')
        for row in myRows:
            row['ctime']=row['ctime'].replace(tzinfo=fromZone)
            row['ctime']=row['ctime'].astimezone(toZone)
            row['ctime']=row['ctime'].strftime('%Y-%m-%d %H:%M:%S')
        errRet={'errno':RET.OK,'errmsg':'查询房源成功','data':myRows}
        return self.write(json.dumps(errRet))

    @require_login
    def post(self):
        userId=self.session.data['userId']
        title=self.get_argument('title')
        price=self.get_argument('price')
        areaId=self.get_argument('area_id')
        address=self.get_argument('address')
        roomCount=self.get_argument('room_count')
        acreage=self.get_argument('acreage')
        houseUnit=self.get_argument('unit')
        capacity=self.get_argument('capacity')
        beds=self.get_argument('beds')
        deposit=self.get_argument('deposit')
        minDays=self.get_argument('min_days')
        maxDays=self.get_argument('max_days')
        faciList=self.get_arguments('facility')
        image=self.request.files.get('house_image')
        imageUrl=None
        if image:
            imageData=image[0].body
            imageName=image[0].filename
            try:
                qiniuUrl=up_load(imageName,imageData)
            except Exception as myError:
                logging.error(myError)
            else:
                imageUrl=QIUNIU_PATH+qiniuUrl
        mySql='insert into ih_house_info(hi_user_id,hi_title,hi_price,hi_area_id,hi_address,hi_room_count,hi_acreage,hi_house_unit,hi_capacity,hi_beds,hi_deposit,hi_min_days,hi_max_days,hi_index_image_url) values(%(user_id)s,%(title)s,%(price)s,%(area_id)s,%(address)s,%(room_count)s,%(acreage)s,%(house_unit)s,%(capacity)s,%(beds)s,%(deposit)s,%(min_days)s,%(max_days)s,%(image_url)s)'
        try:
            houseId=self.db.execute(mySql,user_id=userId,title=title,price=price,area_id=areaId,address=address,room_count=roomCount,acreage=acreage,house_unit=houseUnit,capacity=capacity,beds=beds,deposit=deposit,min_days=minDays,max_days=maxDays,image_url=imageUrl)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'保存房源失败'}
            return self.write(json.dumps(errRet))
        mySql='insert into ih_house_facility(hf_house_id,hf_facility_id) values(%(house_id)s,%(facility_id)s)'
        try:
            for faci in faciList:
                self.db.execute(mySql,house_id=houseId,facility_id=faci)
        except Exception as myError:
            logging.error(myError)
            mySql='delete from ih_house_info where hi_house_id=%(house_id)s'
            try:
                self.db.execute(mySql,house_id=houseId)
            except Exception as myError:
                logging.error(myError)
                errRet={'errno':RET.DBERR,'errmsg':'保存配套失败,删除房源失败'}
                return self.write(json.dumps(errRet))
            errRet={'errno':RET.DBERR,'errmsg':'保存配套失败,删除房源成功'}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'保存房源成功,保存配套成功'}
        self.write(json.dumps(errRet))

class FacilityHandler(BaseHandler):
    """获取/设置配套设施目录"""
    def get(self):
        mySql='select fc_id as id,fc_name as name from ih_facility_catelog'
        try:
            myRows=self.db.query(mySql)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'获取配套失败'}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'获取配套成功','facilitys':myRows}
        return self.write(json.dumps(errRet))

class HouseDetailHandler(BaseHandler):
    """获取/设置房屋详情"""
    def get(self):
        mySession=session.Session(self)
        clientId=mySession.data.get('userId','-1')
        houseId=self.get_argument('house_id')
        mySql='select hi_user_id as user_id,hi_title as title,hi_price as price,hi_address as address,hi_room_count as room_count,hi_acreage as acreage,hi_house_unit as house_unit,hi_capacity as capacity,hi_beds as beds,hi_deposit as deposit,hi_min_days as min_days,hi_max_days as max_days,hi_index_image_url as image_url from ih_house_info where hi_house_id=%(house_id)s'
        try:
            myHouse=self.db.get(mySql,house_id=houseId)
            mySql='select up_name as name from ih_user_profile where up_user_id=%(user_id)s'
            myName=self.db.get(mySql,user_id=myHouse['user_id'])
            myHouse['name']=myName['name']
            myHouse['client_id']=clientId
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'获取房源信息失败','house':None,'facility':None,'avatar':None,'comment':None}
            return self.write(json.dumps(errRet))
        mySql='select hf_facility_id as facility_id from ih_house_facility where hf_house_id=%(house_id)s'
        try:
            myFacilitys=self.db.query(mySql,house_id=houseId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'获取房源配套失败','house':myHouse,'facility':None,'avatar':None,'comment':None}
            return self.write(json.dumps(errRet))
        mySql='select up_avatar as avatar from ih_user_profile where up_user_id=%(user_id)s'
        try:
            myAvatar=self.db.get(mySql,user_id=myHouse['user_id'])
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'获取房东头像失败','house':myHouse,'facility':myFacilitys,'avatar':None,'comment':None}
            return self.write(json.dumps(errRet))
        mySql='select oi_user_id as user_id,oi_comment as comment,oi_ctime as ctime from ih_order_info where oi_house_id=%(house_id)s'
        try:
            myComments=self.db.query(mySql,house_id=houseId)
            fromZone = tz.gettz('UTC')
            toZone = tz.gettz('CST')
            for comment in myComments:
                mySql='select up_name as name from ih_user_profile where up_user_id=%(user_id)s'
                myName=self.db.get(mySql,user_id=comment['user_id'])
                comment['name']=myName['name']
                comment['ctime']=comment['ctime'].replace(tzinfo=fromZone)
                comment['ctime']=comment['ctime'].astimezone(toZone)
                comment['ctime']=comment['ctime'].strftime('%Y-%m-%d %H:%M:%S')
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'获取房源评论失败','house':myHouse,'facility':myFacilitys,'avatar':QIUNIU_PATH+myAvatar['avatar'],'comment':None}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'获取房源信息成功','house':myHouse,'facility':myFacilitys,'avatar':QIUNIU_PATH+myAvatar['avatar'],'comment':myComments}
        return self.write(json.dumps(errRet))
