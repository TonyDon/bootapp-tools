# /bin/python
# -*- coding:utf-8 -*-
import urllib3 
import hashlib
import time, os

appKey = ""
appSecret = ""
accessToken = ""
method = ""
version = "1.0"
format = "json"
signMethod = "md5"
timestamp = ""
param = ""
appSecret = ""

api_gate_url = "https://open.jd.id/api"
api_bigdata_gate_url = "https://open.jd.id/api_bigdata"

urllib3.disable_warnings()
ulreq = urllib3.PoolManager()

def call():
    sys_params = {
        "app_key": appKey,
        "access_token": accessToken,
        "method": method,
        "v": version,
        "format": format,
        "sign_method": signMethod,
        "timestamp": get_server_time(),
        "param_json": param}
    sign = generate_sign(sys_params)
    sys_params["sign"] = sign
    res = ulreq.request('GET', api_gate_url, sys_params, headers=None)
    return res.data.decode('utf-8')

def call_file(filepath):
     file_data = None
     with open(file=filepath, mode='rb') as fp:
         file_data = fp.read()
     file_md5 = hashlib.md5(file_data)
     file_name = os.path.basename(filepath)
     file_mate = (file_name, file_data)
     sys_params = {
        "app_key": appKey,
        "access_token": accessToken,
        "method": method,
        "v": version,
        "format": format,
        "sign_method": signMethod,
        "timestamp": get_server_time(),
        "param_json": param,
        "param_file_md5":file_md5.hexdigest().upper()
        }
     sign = generate_sign(sys_params)
     sys_params["sign"] = sign
     sys_params["param_file"] = file_mate
     res = ulreq.request('POST', api_bigdata_gate_url, sys_params, headers=None)
     return res.data.decode('utf-8')


def get_server_time():
    return time.strftime("%Y-%m-%d %H:%M:%S.000%z", time.localtime())


def generate_sign(sys_params):
    org = appSecret
    data = {}
    key = sorted(sys_params.keys())
    for a in key:
        data[a] = sys_params.get(a)
    print(data)
    for key, value in data.items():
        org = org + key + value
    string = org + appSecret
    m = hashlib.md5(bytes(string, encoding="utf-8"))
    return m.hexdigest().upper()


if __name__ == '__main__':
    appKey = "d5d34d0e8145458612a93526e3ab3616"
    appSecret = "your app secret"
    accessToken = "your access token"
    
    method = "epi.popOrder.getOrderIdListByCondition"
    param = r'{"orderStatus":1,"deliveryType":1,"orderType":3,"startRow":1}'
    print(call())
    
    method="epi.ware.openapi.SpuApi.saveSpuMainPic"
    param = r'{"spuId":12345, "fileName":"out.jpg"}'
    filepath = r'C:\tmp_dir\out.jpg'
    print(call_file(filepath))
    
    ulreq.clear()
