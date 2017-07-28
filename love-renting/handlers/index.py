#-*-coding:utf-8-*-
from handlers.base import BaseHandler
from utils.response_code import *
from contants import *
import logging
import json
import math

class IndexHandler(BaseHandler):
    """获取主页展示房源"""
    def get(self):
        try:
            myIndexs=self.redis.get('indexs')
        except Exception as myError:
            logging.error(myError)
            myIndexs=None
        if myIndexs:
            errRet='{"errno":"0","errmsg":"获取主页房源信息成功","data":%s}' % myIndexs
            return self.write(errRet)
        mySql='select hi_house_id as house_id,hi_title as title,hi_index_image_url as image_url from ih_house_info order by hi_ctime desc limit 0,3'
        try:
            myIndexs=self.db.query(mySql)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'获取主页房源信息失败'}
            return self.write(json.dumps(errRet))
        else:
            try:
                self.redis.setex('indexs',INDEX_EXPIRES,json.dumps(myIndexs))
            except Exception as myError:
                logging.error(myError)
            errRet={'errno':RET.OK,'errmsg':'获取主页房源信息成功','data':myIndexs}
            return self.write(json.dumps(errRet))

class SearchHandler(BaseHandler):
    """获取查询列表页房源结果"""
    def get(self):
        startDate=self.get_argument('sd')
        endDate=self.get_argument('ed')
        areaId=self.get_argument('aid')
        sortKey=self.get_argument('sk')
        page=self.get_argument('p')

        redis_data_key='house_list_%s_%s_%s_%s' % (startDate,endDate,areaId,sortKey)
        try:
            errRet=self.redis.hget(redis_data_key,page)
        except Exception as myError:
            logging.error(myError)
        if errRet:
            return self.write(errRet)

        mySql='select distinct a.hi_house_id,a.hi_title,a.hi_index_image_url,a.hi_price,a.hi_room_count,a.hi_address,a.hi_order_count,b.up_avatar from ih_house_info as a inner join ih_user_profile as b on a.hi_user_id=b.up_user_id'
        totalSql='select count(distinct a.hi_house_id) as counts from ih_house_info as a inner join ih_user_profile as b on a.hi_user_id=b.up_user_id'

        sqlWhere=[]
        sqlVal={}

        if startDate and endDate:
            sqlWhere.append('a.house_id not in (select oi_house_id from ih_order_info where oi_begin_date<=%(end_date)s and oi_end_date>=%(start_date)s)')
            sqlVal['start_date']=startDate
            sqlVal['end_date']=endDate
        elif startDate:
            sqlWhere.append('a.house_id not in (select oi_house_id from ih_order_info where oi_end_date>=%(start_date)s)')
            sqlVal['start_date']=startDate
        elif endDate:
            sqlWhere.append('a.house_id not in (select oi_house_id from ih_order_info where oi_begin_date<=%(end_date)s')
            sqlVal['end_date']=endDate

        if areaId:
            sqlWhere.append('a.hi_area_id=%(area_id)s')
            sqlVal['area_id']=areaId

        if sqlWhere:
            mySql+=' where '
            totalSql+=' where '
            mySql+=' and '.join(sqlWhere)
            totalSql+=' and '.join(sqlWhere)

        totalPage=-1
        try:
            myRow=self.db.get(totalSql,**sqlVal)
        except Exception as myError:
            logging.error(myError)
        else:
            totalPage=int(math.ceil(myRow['counts']/float(SEARCH_PAGE_CAPACITY)))
        page=int(page)
        if totalPage!=-1 and page>totalPage:
            errRet={'errno':RET.OK,'errmsg':'无更多房源数据','data':[],'total_page':totalPage}
            return self.write(json.dumps(errRet))

        if sortKey=='new':
            mySql+=' order by a.hi_ctime desc'
        if sortKey=='booking':
            mySql+=' order by a.hi_order_count desc'
        if sortKey=='price-inc':
            mySql+=' order by a.hi_price asc'
        if sortKey=='price-des':
            mySql+=' order by a.hi_price desc'

        mySql+=' limit %d,%d' %((page-1)*SEARCH_PAGE_CAPACITY,SEARCH_PAGE_CAPACITY*SEARCH_REDIS_PAGE)
        try:
            myRows=self.db.query(mySql,**sqlVal)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'查询房源数据失败','data':[],'total_page':totalPage}
            return self.write(json.dumps(errRet))
        houses=[]
        if myRows:
            for row in myRows:
                data={
                    'house_id':row['hi_house_id'],
                    'title':row['hi_title'],
                    'image_url':row['hi_index_image_url'],
                    'price':row['hi_price'],
                    'room_count':row['hi_room_count'],
                    'address':row['hi_address'],
                    'order_count':row['hi_order_count'],
                    'avatar':QIUNIU_PATH+row['up_avatar'],
                }
                houses.append(data)
        else:
            errRet={'errno':RET.OK,'errmsg':'无符合条件房源','data':[],'total_page':totalPage}
            return self.write(json.dumps(errRet))

        redis_data={}
        i=0
        while True:
            page_data=houses[i*SEARCH_PAGE_CAPACITY:(i+1)*SEARCH_PAGE_CAPACITY]
            if not page_data:
                break
            errRet={'errno':RET.OK,'errmsg':'查询房源成功','data':page_data,'total_page':totalPage}
            redis_data[str(page+i)]=json.dumps(errRet)
            i+=1
        try:
            self.redis.hmset(redis_data_key,redis_data)
            self.redis.expire(redis_data_key,SEARCH_PAGE_EXPIRES)
        except Exception as myError:
            logging.error(myError)

        self.write(redis_data[str(page)])
