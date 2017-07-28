#-*-coding:utf-8-*-
from base import BaseHandler
from utils.response_code import *
from utils.session import Session
from datetime import datetime
import logging
import json


class BookingHandler(BaseHandler):
    """获取/提交预定页信息"""
    def get(self):
        houseId=self.get_argument('id')
        mySql='select hi_house_id as house_id,hi_user_id as user_id,hi_title as title ,hi_price as price ,hi_index_image_url as image_url from ih_house_info where hi_house_id=%(house_id)s'
        try:
            myRow=self.db.get(mySql,house_id=houseId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'查询房源信息失败'}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'查询房源信息成功','data':myRow}
        return self.write(json.dumps(errRet))

    def post(self):
        mySession=Session(self)
        userId=mySession.data['userId']
        houseId=self.dict.get('house_id')
        startDate=self.dict.get('start_date')
        endDate=self.dict.get('end_date')

        if not all([houseId,startDate,endDate]):
            errRet={'errno':RET.PARAMERR,'errmsg':'参数获取失败'}
            return self.write(json.dumps(errRet))

        mySql='select hi_price as price,hi_user_id as user_id from ih_house_info where hi_house_id=%(house_id)s'
        try:
            myHouse=self.db.get(mySql,house_id=houseId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'获取预定房源信息失败'}
            return self.write(json.dumps(errRet))
        if not myHouse:
            errRet={'errno':RET.NODATA,'errmsg':'预定的房源不存在'}
            return self.write(json.dumps(errRet))

        if userId==myHouse['user_id']:
            errRet={'errno':RET.ROLEERR,'errmsg':'不可以预定自己的房源'}
            return self.write(json.dumps(errRet))

        orderDays=(datetime.strptime(endDate,'%Y-%m-%d')-datetime.strptime(startDate,'%Y-%m-%d')).days+1
        if orderDays<=0:
            errRet={'errno':RET.PARAMERR,'errmsg':'预定日期不符合要求'}
            return self.write(json.dumps(errRet))

        mySql='select count(*) as counts from ih_order_info where oi_house_id=%(house_id)s and oi_begin_date>=%(end_date)s and oi_end_date>=%(start_date)s'
        try:
            myRow=self.db.get(mySql,house_id=houseId,start_date=startDate,end_date=endDate)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'查询房源现有订单信息失败'}
            return self.write(json.dumps(errRet))
        if myRow['counts']>0:
            errRet={'errno':RET.DATAERR,'errmsg':'该房源已经被预定'}
            return self.write(json.dumps(errRet))

        totalFee=orderDays*myHouse['price']
        mySql='insert into ih_order_info(oi_user_id,oi_house_id,oi_begin_date,oi_end_date,oi_days,oi_house_price,oi_amount) values(%(user_id)s,%(house_id)s,%(start_date)s,%(end_date)s,%(days)s,%(price)s,%(amount)s);' \
              'update ih_house_info set hi_order_count=hi_order_count+1 where hi_house_id=%(house_id)s;'
        try:
            self.db.execute(mySql,user_id=userId,house_id=houseId,start_date=startDate,end_date=endDate,days=orderDays,price=myHouse['price'],amount=totalFee)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'预定失败'}
            return self.write(json.dumps(errRet))

        errRet={'errno':RET.OK,'errmsg':'预定成功'}
        return self.write(json.dumps(errRet))

class OrderHandler(BaseHandler):
    """获取/设置订单页信息"""
    def get(self):
        mySession=Session(self)
        userId=mySession.data['userId']
        role=self.get_argument('role')
        if role=='tenant':
            mySql='select oi_order_id,hi_title,hi_index_image_url,oi_begin_date,oi_end_date,oi_ctime,oi_days,oi_amount,oi_status,oi_comment,up_name from ih_order_info inner join ih_house_info on oi_house_id=hi_house_id left join ih_user_profile on hi_user_id=up_user_id where oi_user_id=%(user_id)s order by oi_ctime desc'
        else:
            mySql='select oi_order_id,hi_title,hi_index_image_url,oi_begin_date,oi_end_date,oi_ctime,oi_days,oi_amount,oi_status,oi_comment,up_name from ih_order_info inner join ih_house_info on oi_house_id=hi_house_id left join ih_user_profile on oi_user_id=up_user_id where hi_user_id=%(user_id)s order by oi_ctime desc'
        try:
            myOrders=self.db.query(mySql,user_id=userId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'查询订单信息失败'}
            return self.write(json.dumps(errRet))
        orders=[]
        for order in myOrders:
            data={
                "order_id": order["oi_order_id"],
                "title": order["hi_title"],
                "img_url":order["hi_index_image_url"],
                "start_date": order["oi_begin_date"].strftime("%Y-%m-%d"),
                "end_date": order["oi_end_date"].strftime("%Y-%m-%d"),
                "ctime": order["oi_ctime"].strftime("%Y-%m-%d %H:%M:%S"),
                "days": order["oi_days"],
                "amount": order["oi_amount"],
                "status": order["oi_status"],
                "name":order["up_name"],
                "comment": order["oi_comment"],
            }
            orders.append(data)
        errRet={'errno':RET.OK,'errmsg':'查询订单信息成功','data':orders}
        return self.write(json.dumps(errRet))

    def put(self):
        mySession=Session(self)
        userId=mySession.data["userId"]
        orderId=self.dict.get("order_id")
        action=self.dict.get("action")

        if not all([orderId, action]):
            return self.write(json.dumps({"errno": RET.PARAMERR, "errmsg": "参数异常"}))

        if "accept" == action:
            mySql="update ih_order_info set oi_status=1 where oi_order_id=%(order_id)s and oi_house_id in (select hi_house_id from ih_house_info where hi_user_id=%(user_id)s) and oi_status=0"
            try:
                # 确保房东只能修改属于自己房子的订单
                self.db.execute(mySql,order_id=orderId, user_id=userId)
            except Exception as myError:
                logging.error(myError)
                return self.write(json.dumps({"errno": RET.DBERR, "errmsg": "数据提交失败"}))
        elif "reject" == action:
            reject_reason = self.dict.get("reject_reason")
            if not reject_reason:
                return self.write(json.dumps({"errno": RET.PARAMERR, "errmsg": "没有拒单理由"}))
            mySql="update ih_order_info set oi_status=6,oi_comment=%(reject_reason)s where oi_order_id=%(order_id)s and oi_house_id in (select hi_house_id from ih_house_info where hi_user_id=%(user_id)s) and oi_status=0"
            try:
                self.db.execute(mySql,reject_reason=reject_reason, order_id=orderId, user_id=userId)
            except Exception as myError:
                logging.error(myError)
                return self.write(json.dumps({"errno": RET.DBERR, "errmsg": "数据提交失败"}))

        self.write(json.dumps({"errno": RET.OK, "errmsg": "数据提交成功"}))

