# -*- coding: utf-8 -*-
from qiniu import Auth, put_data

def up_load(fileName,fileData):
    #需要填写你的 Access Key 和 Secret Key
    access_key = 'uXd6mLbp5Re_L22b0ju2v0pMYD24q6SewSJDXwEH'
    secret_key = '-6wIibcz7mgi4rQUwgg4zY0cbFPyOA2kpIsMsfTi'
    #构建鉴权对象
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = 'ihome'
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)
    ret, info = put_data(token, None, fileData)
    if info.status_code!=200:
        raise Exception('上传失败')
    else:
        return ret['hash']

if __name__=='__main__':
    with open('../../static/images/home01.jpg') as myFile:
        fileName=myFile.name
        fileData=myFile.read()
        up_load(fileName,fileData)