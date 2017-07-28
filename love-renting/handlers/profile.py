#-*-coding:utf-8-*-
from handlers.base import BaseHandler
from utils.response_code import *
from libs.qiniu.upload import up_load
from utils.common import require_login
from contants import *
import json
import logging

class AvatarHandler(BaseHandler):
    """用户头像上传"""
    @require_login
    def put(self):
        userId=self.session.data['userId']
        avatar=self.request.files.get('avatar')
        if not avatar:
            errRet={'errno':RET.PARAMERR,'errmsg':'未上传头像'}
            return self.write(json.dumps(errRet))
        avatarData=avatar[0].body
        fileName=avatar[0].filename
        try:
            avatarPath=up_load(fileName,avatarData)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.THIRDERR,'errmsg':'上传七牛失败'}
            return self.write(json.dumps(errRet))
        mySql='update ih_user_profile set up_avatar=%(avatar)s where up_user_id=%(user_id)s'
        try:
            self.db.execute(mySql,avatar=avatarPath,user_id=userId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'存储头像失败'}
            return self.write(json.dumps(errRet))
        errRet={
            'errno':RET.OK,
            'errmsg':'头像保存成功',
            'avatarUrl':QIUNIU_PATH+avatarPath,
        }
        self.write(json.dumps(errRet))

class UserInfoHandler(BaseHandler):
    """获取/修改登陆后的用户个人信息"""
    @require_login
    def get(self):
        userId=self.session.data['userId']
        mySql='select up_name as name,up_mobile as mobile,up_avatar as avatarPath from ih_user_profile where up_user_id=%(user_id)s'
        try:
            myRow=self.db.get(mySql,user_id=userId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'头像读取失败','name':name,'mobile':mobile,'avatar':None}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'头像读取失败','name':myRow['name'],'mobile':myRow['mobile'],'avatar':QIUNIU_PATH+myRow['avatarPath']}
        return self.write(json.dumps(errRet))

    @require_login
    def put(self):
        userId=self.session.data['userId']
        userName=self.get_argument('name')
        mySql='update ih_user_profile set up_name=%(name)s where up_user_id=%(user_id)s'
        try:
            self.db.execute(mySql,name=userName,user_id=userId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'保存用户名出错'}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'保存用户名成功'}
        return self.write(json.dumps(errRet))

class AuthHandler(BaseHandler):
    """获取/设置实名认证信息"""
    @require_login
    def get(self):
        userId=self.session.data['userId']
        mySql='select up_real_name as real_name,up_id_card as id_card from ih_user_profile where up_user_id=%(user_id)s'
        try:
            myRow=self.db.get(mySql,user_id=userId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'查询数据库失败'}
            return self.write(json.dumps(errRet))
        if not all([myRow['real_name'],myRow['id_card']]):
            errRet={'errno':RET.NODATA,'errmsg':'未实名认证'}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'已实名认证','realName':myRow['real_name'],'idCard':myRow['id_card']}
        return self.write(json.dumps(errRet))

    @require_login
    def put(self):
        userId=self.session.data['userId']
        realName=self.get_argument('real_name')
        idCard=self.get_argument('id_card')
        mySql='update ih_user_profile set up_real_name=%(real_name)s,up_id_card=%(id_card)s where up_user_id=%(user_id)s'
        try:
            self.db.execute(mySql,real_name=realName,id_card=idCard,user_id=userId)
        except Exception as myError:
            logging.error(myError)
            errRet={'errno':RET.DBERR,'errmsg':'保存实名信息异常'}
            return self.write(json.dumps(errRet))
        errRet={'errno':RET.OK,'errmsg':'保存实名信息成功'}
        return self.write(json.dumps(errRet))
