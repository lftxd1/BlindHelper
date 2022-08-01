# -*-coding:utf-8-*-
import uuid
import requests
import json
import hmac
from hashlib import sha1
from hashlib import sha256
import urllib
import copy
import time
import random
from pydub import AudioSegment
import wave
# 填写您的accesskey 和secretKey
import base64
access_key ="f40fb1ac57474d5ba8e7ca2bfe469f75"

secret_key = "7685f7710a3a4ed5a3a468a11a90ccee"


# 签名计算
def sign(http_method, playlocd, servlet_path):
    time_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    playlocd['Timestamp'] = time_str
    parameters = copy.deepcopy(playlocd)
    parameters.pop('Signature')
    sorted_parameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalized_query_string = ''
    for (k, v) in sorted_parameters:
        canonicalized_query_string += '&' + percent_encode(k) + '=' + percent_encode(v)
    string_to_sign = http_method + '\n'  + percent_encode(servlet_path) + '\n' + sha256(canonicalized_query_string[1:].encode('utf-8')).hexdigest()
    key = ("BC_SIGNATURE&" + secret_key).encode('utf-8')
    string_to_sign = string_to_sign.encode('utf-8')
    signature = hmac.new(key, string_to_sign, sha1).hexdigest()
    return signature

# 参数编码
def percent_encode(encode_str):
    encode_str = str(encode_str)
    res = urllib.parse.quote(encode_str.encode('utf-8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

def D_BASE64(origStr):
    #当输入的base64字符串不是3的倍数时添加相应的=号
    if(len(origStr)%3 == 1): 
        origStr += "=="
    elif(len(origStr)%3 == 2): 
        origStr += "=" 
    return origStr

import wave

def generate_random_str(randomlength=16):
  """
  生成一个指定长度的随机字符串
  """
  random_str =''
  base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length =len(base_str) -1
  for i in range(randomlength):
    random_str +=base_str[random.randint(0, length)]
  return random_str


def TxtToMp3():
    # http method
    method = 'POST'
    # 目标域名 端口
    url = "https://api-wuxi-1.cmecloud.cn:8443"
    # 请求url
    path = '/api/lingxiyun/cloud/iat/send_request/v1'
    # 可以不改
    headers = {'Content-Type': 'application/json',"streamId":"qwew","number":"1","Language":"cn"}
    # 签名公参，如果有其他参数，同样在此添加
    querystring = {"AccessKey": access_key, "Timestamp": "2020-12-11T16:27:01Z", "Signature": "", "SignatureMethod": "HmacSHA1", "SignatureNonce": "", "SignatureVersion": "V2.0"}
    # 请求body
    import base64
    f1=open('../test.pcm', 'rb') 
    base64_str = base64.b64encode(f1.read())  # str类型
    payload = {
	"data":str(base64_str),
    "endFlag":1,
    "sessionParam":{
            "sid":"2",
            "aue":"raw",  
            "eos":"1",
            "bos":"1",
            "rate":"16000",
            "hotword":"",
    }
    }
    
    # 生成SignatureNonce
    querystring['SignatureNonce'] = uuid.uuid4()
    # 生成签名
    querystring['Signature'] = sign(method, querystring, path)
    test = requests.request(method, url + path, headers=headers, params=querystring, json=payload)
    import base64
    result = json.loads(test.text)
    print(result)


TxtToMp3()