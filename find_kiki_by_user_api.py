import requests
from urllib.error import URLError
import urllib.request as urlrequest
import requests
import json
import time
import csv

# 待测试目标网页
targetUrl = "http://icanhazip.com"
user_api_url = 'https://api.douban.com/v2/user/{}'
start_num = 1000004
end_num = 147674899#数据不准确
#end_num = 1000009

#fp = open("iplist.txt",'r')
#lines = fp.readlines()

def get_proxies():
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H1BADAR144FE21WD"
    proxyPass = "C498F743624B94D9"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }
    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    return proxies

with open('result.csv', 'w', encoding='utf8') as outputfile:
    writer = csv.writer(outputfile)
    proxy = get_proxies()
    requests.packages.urllib3.disable_warnings()
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    while start_num <= end_num:
        try:
            #伪装成浏览器
            #opener.addheaders = [('User-Agent',
            #                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
            print("请求页面" + user_api_url.format(start_num))
            time.sleep(1)
            movies_content = requests.get(user_api_url.format(start_num), proxies = proxy, verify=False)
            if movies_content.status_code == 200:
                # 页面解析
                json_text = json.loads(movies_content.text)
                user_name = json_text['name']
                user_sid = json_text['id']
                user_avatar_url = json_text['large_avatar']
                user_url = json_text['alt']
                if 'Kiki' in user_name:
                    urlrequest.urlretrieve(user_avatar_url, ".\\icon\%s.jpg" % (list))
                    outputfile.write('{}#{}\n'.format(user_name, user_sid))
                print(user_name)
                movies_content.close()
            else:
                errorMsg = movies_content.text
                print("报错信息: " + errorMsg)
                if errorMsg != '':
                    json_error = json.loads(errorMsg)
                    if json_error['code'] == 112:
                        print("访问太频繁了, 退出!" + start_num)
                        break
        except Exception as e:
            print("异常: " + str(e.args))
            continue
        #用户ID增长
        start_num = start_num + 1
#print("报错信息" + json_error['msg'])