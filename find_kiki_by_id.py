import urllib.request as urlrequest
from bs4 import BeautifulSoup
import json
import time
import csv

#user_url = 'https://api.douban.com/v2/user/{}'
#user_url = 'https://www.douban.com/people/{}/'
start_num = 1000001
end_num = 147674899   #数据不准确
#end_num = 1000002

with open('result.csv', 'w', encoding='utf8') as outputfile:
    writer = csv.writer(outputfile)
    for list in range(start_num, end_num):
        print("请求页面" + user_url.format(list))
        time.sleep(5)
        movies_content = urlrequest.urlopen(user_url.format(list)).read()
        movies_html = movies_content.decode('utf8')
        moviessoup = BeautifulSoup(movies_html, 'html.parser')
        db_user_profile = moviessoup.find(class_='clearfix')
        sun_ins_content = db_user_profile.find(class_='info')
        name_h1 = sun_ins_content.h1.text
        #尝试获取用户签名, 有可能没有
        try:
            user_desc = sun_ins_content.find(class_='signature_display pl')
            if user_desc!='':
                user_desc = user_desc.text.strip()
        except Exception as e:
            user_desc = 'None'
        #尝试去掉名字中的签名数据
        nick_name = name_h1.replace(user_desc, ' ')
        #去掉无关字符
        nick_name = nick_name.replace("\n", " ")
        nick_name = nick_name.replace(" ", "")
        nick_name = nick_name.strip()
        print('去掉之后: ' + nick_name)
        if 'Kiki' in nick_name:
            #获取头像url
            pic_url = db_user_profile.find(class_='pic')
            pic_url = pic_url.find('img').get('src')
            urlrequest.urlretrieve(pic_url, ".\\icon\%s.jpg" % (list))
            print(pic_url)
            outputfile.write('{}#{}\n'.format(nick_name, pic_url))