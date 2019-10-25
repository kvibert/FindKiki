import urllib.request as urlrequest
from bs4 import BeautifulSoup
import json
import time
import csv

search_url = 'https://www.douban.com/search?cat=1005&q=kiki'
search_url_more = 'https://www.douban.com/j/search?q=Kiki&start={}&cat=1005'
search_url_more = 'https://api.douban.com/v2/user?q=kiki&start={}'
user_url = 'https://www.douban.com/people/{}/'

# print('{} {} {} {} {}'.format(movie_name,movie_assess,movie_score,movie_url,movie_intro))
with open('result.csv', 'w', encoding='utf8') as outputfile:
    # outputfile.write(codecs.BOM_UTF8)
    writer = csv.writer(outputfile)
    # writer.writerow(["movie_num","movie_name","movie_assess","movie_score","movie_url","movie_intro"])
    #outputfile.write("movie_num#movie_name#movie_year#movie_country#movie_type#movie_director#movie_assess#movie_score#movie_url#movie_intro\n")
    for list in range(101):
        current_page = 0
        current_page = list * 20
        print("请求页面" + search_url_more.format(current_page))
        time.sleep(1)
        movies_content = urlrequest.urlopen(search_url_more.format(current_page)).read()
        movies_html = movies_content.decode('utf8')
        json_text = json.loads(movies_html)
        #moviessoup = BeautifulSoup(movies_html, 'html.parser')
        #all_list = moviessoup.find_all(class_='result')
        #print(movies_html)
        for item in json_text['items']:
            moviessoup = BeautifulSoup(item, 'html.parser')
            all_list = moviessoup.find_all(class_='result')
            for result in all_list:
                item_content = result.find(class_='content')
                try:
                    user_desc = item_content.find('p').text.strip()
                    user_desc = user_desc.replace("\n", " ")
                    user_desc = user_desc.replace("\r", " ")
                    user_desc = user_desc.replace(" ","")
                except Exception as e:
                    user_desc = 'None'
                item_data = item_content.find(class_='title')
                user_name = item_data.find('a').text
                if user_name == 'Kiki':
                #if '重庆' in user_info:
                    user_temp_url = item_data.find('a')['onclick']
                    # 截取Json字符串
                    sid_index = user_temp_url.index('sid')
                    qcat_index = user_temp_url.index('qcat')
                    user_sid = user_temp_url[sid_index + 4: qcat_index - 2]
                    user_sid = user_sid.strip()
                    #下载头像
                    img_url = result.find('img').get('src')
                    #urlrequest.urlretrieve(img_url, ".\\icon\%s.jpg" % (user_sid))
                    user_info = item_data.find(class_='info').text.strip()

                    outputfile.write('{}#{}#{}#{}\n'.format(user_name, user_info, user_desc, user_url.format(user_sid)))
                    #print(user_info)

