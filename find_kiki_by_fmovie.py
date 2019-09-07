import urllib.request as urlrequest
import urllib.parse as urlparse
from bs4 import BeautifulSoup
from http import cookiejar
import time
import csv

url_login = 'https://accounts.douban.com/j/mobile/login/basic'
#电影名称
fmovie_url1 = 'https://movie.douban.com/subject/26794435/collections?start={}'
# print('{} {} {} {} {}'.format(movie_name,movie_assess,movie_score,movie_url,movie_intro))
with open('result.csv', 'w', encoding='utf8') as outputfile:
    # outputfile.write(codecs.BOM_UTF8)
    writer = csv.writer(outputfile)
    #模拟登录

    # 创建Cookie
    cookie_object = cookiejar.CookieJar()
    # handler 对应着一个操作
    handler = urlrequest.HTTPCookieProcessor(cookie_object)
    # opener 遇到有cookie的response的时候,
    # 调用handler内部的一个函数, 存储到cookie object
    openner = urlrequest.build_opener(handler)
    # 添加headers
    openner.addheaders = [('User-agent',
                           'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
    data = {
        'ck': '',
        'name': 'username', #用户名
        'password': 'password', #密码
        'remember': 'false',
        'ticket': ''
    }
    # post
    form_bytes = urlparse.urlencode(data).encode('utf-8')
    response = openner.open(url_login, form_bytes)
    html_bytes = response.read()
    # writer.writerow(["movie_num","movie_name","movie_assess","movie_score","movie_url","movie_intro"])
    #outputfile.write("movie_num#movie_name#movie_year#movie_country#movie_type#movie_director#movie_assess#movie_score#movie_url#movie_intro\n")
    for list in range(181): #17550
        current_page = 0
        current_page = list * 20
        print("当前的页数是" + fmovie_url1.format(current_page))
        time.sleep(1)
        response = openner.open(fmovie_url1.format(current_page))
        movies_content = response.read()
        #movies_content = urlrequest.urlopen(fmovie_url1.format(current_page)).read()
        movies_html = movies_content.decode('utf8')
        moviessoup = BeautifulSoup(movies_html, 'html.parser')
        sun_ins_content = moviessoup.find(class_='sub_ins')
        # 获取所有table元素
        table_list = sun_ins_content.findAll('table')
        for item in table_list:
            tb_list = item.findAll('td')
            try:
                nick_name_td = tb_list[1]
                nick_name = nick_name_td.find('a').text
                nick_name = nick_name.replace("\n", " ")
                nick_name = nick_name.replace(" ", "")
                nick_name = nick_name.strip()
            except Exception as e:
                nick_name = 'None'
            #找出昵称中有Kiki的用户
            if 'Kiki' in nick_name:
                #获取用户url
                user_url = nick_name_td.find('a').get('href')
                outputfile.write('{}#{}\n'.format(nick_name, user_url))
