from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pymysql
import requests
import sqlite3
import os

# 初始化数据库连接
connection = pymysql.connect(host='35.201.154.5',
                             user='indubao',
                             password='123456',
                             database='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# 创建一个数据库游标
cursor = connection.cursor()


# 设置 Chrome 驱动器选项
#chrome_path = '/usr/local/bin/chromedriver'
#os.environ['webdriver.chrome.driver'] = chrome_path
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--silent")
chrome_options.add_argument("--headless")

#service = Service(chrome_path)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 爬取豆瓣电影页面
url = "https://movie.douban.com/"
driver.get(url)
new_page_html = driver.page_source
soup = BeautifulSoup(new_page_html, 'html.parser')

# 遍历热门电影
for a in range(5):
    hot_movie = soup.find_all(class_="slide-page")[a]
    for movie_data in hot_movie.find_all("a", class_="item"):
        # 初始化电影信息
        href = movie_data["href"]
        img_tag = movie_data.find("img")
        scr = img_tag["src"]
        response = requests.get(scr)
        image_data = response.content
        name = img_tag["alt"]
        genre = runtime = country = language = director = writer = aliases = imdb_id = ''
        release_dates = []

        driver.get(href)
        new_page_from_movie = driver.page_source
        movie = BeautifulSoup(new_page_from_movie, 'html.parser')
        ppp = movie.find_all(class_="attrs", limit=2)
        pl = movie.find_all(class_="pl")

        # 获取电影属性
        property_data = ["v:genre", "v:runtime"]
        for prop in property_data:
            prop_span = movie.find("span", property=prop)
            if prop_span:
                if prop == "v:genre":
                    genre = prop_span.text.strip()
                elif prop == "v:runtime":
                    runtime = prop_span.text.strip()

        # 获取上映日期
        release_date_spans = movie.find_all("span", property="v:initialReleaseDate")
        for date_span in release_date_spans:
            release_dates.append(date_span.text.strip())

        for a in ppp :
            director = a.text.strip()[0]
            writer = a.text.strip()[1]



        # 获取其他信息
        cm = ["制片国家/地区:", "语言:", "又名:", "IMDb:"]
        for aaa in cm:
            if aaa == "制片国家/地区:":
                country_tag = movie.find("span", class_="pl", string="制片国家/地区:")
                if country_tag:
                    country = country_tag.next_sibling.strip()
            elif aaa == "语言:":
                language_tag = movie.find("span", string="语言:")
                if language_tag:
                    language = language_tag.next_sibling.strip()
            elif aaa == "又名:":
                aliases_tag = movie.find("span", string="又名:")
                if aliases_tag:
                    aliases = aliases_tag.next_sibling.strip()
            elif aaa == "IMDb:":
                imdb_tag = movie.find("span", string="IMDb:")
                if imdb_tag:
                    imdb_id = imdb_tag.next_sibling.strip()

        print(country,language,aliases,imdb_id)

        # 将数据插入数据库
        cursor.execute('''INSERT INTO new_movies2 
                          (電影名 ,海報 ,鏈接 , 類型, 片長, 制片國家, 語言, 上映日期, 導演, 編劇, 別名, IMDb編號) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (name, image_data, href, genre, runtime, country, language, ','.join(release_dates),
                        director, writer, aliases, imdb_id))

        # 提交更改并关闭连接
        connection.commit()

        driver.back()

# 关闭数据库连接
connection.close()
