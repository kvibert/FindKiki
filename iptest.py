import requests
# 待测试目标网页
targetUrl = "http://icanhazip.com"
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

    for i in range(1,6):
        resp = requests.get(targetUrl, proxies=proxies)
        # print(resp.status_code)
        print('第%s次请求的IP为：%s'%(i,resp.text))
get_proxies()
