import requests
# urllib
import datetime
from common import util
import json



def sendSMS(body, phoneNO):
    url = "https://api.miaodiyun.com/20150822/industrySMS/sendSMS"
    accountSid = "28ce762151b546a9be100f377b5c20f6"
    authtoken = "b97ec0e33eaa40f68efdc23eeac57494"
    smsconet = "【F-Blog博客】您的验证码为%s，5分钟后失效，您正在修改登录密码，请确认是本人操作。" % body
    to = phoneNO
    tims = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    sig = util.getMd5(accountSid + authtoken + tims)
    data = {"accountSid": accountSid, "smsContent": smsconet, "to": to, "timestamp": tims, "sig": sig}
    r = requests.post(url, data)
    r2 = json.loads(r.content.decode('utf-8'))
    if r2["respCode"] == "00000":
        return True
    else:
        return False
