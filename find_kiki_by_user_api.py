from queue import Queue
import requests
import threading
import json
import time
import copy
import csv

# 待测试目标网页
targetUrl = "http://icanhazip.com"
user_api_url = 'https://api.douban.com/v2/user/%d'
#start_num = 1002181
start_num = 81800000  #2014
end_num = 120000000 #2015/12/14

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
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


class DoubanSpider(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }

    def __init__(self, page_queue, user_queue, *args, **kwargs):
        super(DoubanSpider, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.user_queue = user_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            #获取代理IP
            proxy = get_proxies()
            requests.packages.urllib3.disable_warnings()
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            #获取URL
            url = self.page_queue.get()
            currentUrl = copy.copy(url)
            print(currentUrl)
            #print("当前访问的URL是: " + str(threading.current_thread()) + "线程名: " + currentUrl)
            try:
                movies_content = requests.get(currentUrl, proxies=proxy, verify=False, headers=self.headers)
                if movies_content.status_code == 200:
                    # 页面解析
                    json_text = json.loads(movies_content.text)
                    user_name = json_text['name']
                    user_sid = json_text['id']
                    user_avatar_url = json_text['avatar']
                    #print("当前URL: " + user_avatar_url)
                    #user_url = json_ text['alt']
                    if 'Kiki' in user_name:
                        self.user_queue.put((user_sid, user_avatar_url))
                movies_content.close()
            except Exception as e:
                #重新放入URL
                #print("解析异常: " + str(e.args))
                #print("重新放入URL: " + str(threading.current_thread()) + "线程名: " + currentUrl)
                self.page_queue.put(currentUrl)


class IconWriter(threading.Thread):
    def __init__(self, user_queue,  writer, gLock, *args, **kwargs):
        super(IconWriter, self).__init__(*args, **kwargs)
        self.user_queue = user_queue
        self.writer = writer
        self.lock = gLock

    def run(self):
        while True:
            try:
                user_info = self.user_queue.get(timeout=40)
                user_sid, user_avatar_url = user_info
                self.lock.acquire()
                self.writer.writerow((user_sid, user_avatar_url))
                self.lock.release()
                #print('保存一条')
            except Exception as e:
                print("下载异常: " + user_sid + str(e.args))
                break


def main():
    number = end_num - start_num
    page_queue = Queue(number)
    #print("当前访问数: " + str(number))
    user_queue = Queue(number)
    fp = open('result.csv', 'w', encoding='utf8', newline='')
    writer = csv.writer(fp)
    writer.writerow(('user_sid', 'user_avatar_url'))

    gLock = threading.Lock()

    for x in range(start_num, start_num + 100):
        url = user_api_url % x
        #print("当前要获取的地址是: " + url)
        page_queue.put(url)

    print("初始化完成")

    for x in range(5):
        t = DoubanSpider(page_queue, user_queue)
        t.start()

    for x in range(5):
        t = IconWriter(user_queue, writer, gLock)
        t.start()

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    #print("程序耗时%f秒." % (end_time - start_time))