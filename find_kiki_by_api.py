import urllib.request as urlrequest
from bs4 import BeautifulSoup
import json
import time
import csv

search_url = 'https://api.douban.com/v2/user?q=kiki&start={}'
user_url = 'https://www.douban.com/people/{}/'

with open('result.csv', 'w', encoding='utf8') as outputfile:
    writer = csv.writer(outputfile)
    for list in range(70, 101):
        current_page = 0
        current_page = list * 20
        print("当前页数是: " + str(current_page))
        print("请求页面" + search_url.format(current_page))
        time.sleep(1)
        movies_content = urlrequest.urlopen(search_url.format(current_page)).read()
        movies_html = movies_content.decode('utf8')
        json_text = json.loads(movies_html)
        for item in json_text['users']:
            #获取name
            user_name = item['name']
            user_sid = item['id']
            user_avatar = item['large_avatar']
            user_url = item['alt']
            user_desc = item['desc'].strip()
            user_desc = user_desc.replace("\n", " ")
            user_desc = user_desc.replace("\r", " ")
            user_desc = user_desc.replace(" ", "")
            if user_name == 'Kiki':
                #下载头像
                urlrequest.urlretrieve(user_avatar, ".\\icon\%s.jpg" % (user_sid))
                outputfile.write('{}#{}#{}\n'.format(user_name, user_desc, user_url.format(user_sid)))

