# -*- coding: UTF-8 -*-
# @Author: Mr. Li
# @Date: 2023/5/14 12:28

import json
import pymysql
import urllib.request
from datetime import datetime


class Spider(object):
    """ 爬取豆瓣电影排行榜 """

    def __init__(self, urls: list, headers: dict = None):
        # 传递要爬取的URL列表
        self.urls = urls
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/110.0.0.0 Safari/537.36',
        }

    def get_data(self) -> dict:
        """
        提取并整理电影数据字段
        :return: {排名:1, 标题:url ...}
        """
        for url in self.urls:
            request = urllib.request.Request(url=url, headers=self.headers)
            response = urllib.request.urlopen(url=request)
            # 提取出响应的内容
            content = response.read()
            content = content.decode('utf-8')  # json格式
            # 解析json为list
            movies = json.loads(content, strict=False)
            # 定义字典存储每个电影的数据
            data = dict()
            for movie in movies:
                try:
                    data['rank'] = int(movie['rank'])  # 排名
                    data['score'] = float(movie['score'])  # 评分
                    data['title'] = movie['title'].replace("\"", "\\\"")  # 电影名
                    data['types'] = ', '.join(movie['types'])  # 类型
                    data['cover_url'] = movie['cover_url']  # 海报
                    data['release_date'] = datetime.strptime(movie['release_date'], '%Y-%m-%d').date()  # 上映时间
                    data['regions'] = ', '.join(movie['regions'])  # 地区
                    data['actor_count'] = int(movie['actor_count'])  # 主演数量
                    data['actors'] = ', '.join(movie['actors']).replace("\"", "\\\"")  # 演员列表
                    data['movie_url'] = movie['url']  # 详情页链接
                    data['vote_count'] = int(movie['vote_count'])  # 评价人数
                except:
                    pass
                yield data


class WriteSQL():
    """ 将Spider返回的数据写入数据库中 """

    def __init__(self, host='localhost', user='root', password='python', database='doubanmovies', table_name=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table_name = table_name  # 数据表名

    def myconnect(self):
        # 创建数据库连接
        self.db = pymysql.connect(
            host=self.host,
            port=3306,
            user=self.user,
            password=self.password,
            db=self.database,
            charset='utf8'
        )
        self.cursor = self.db.cursor()

    def myinsert(self, data):
        self.data = data
        sql = 'insert into {} values(null, {}, {}, "{}", "{}", "{}", "{}", "{}", {}, "{}", "{}", {});'.format(
            self.table_name, self.data['rank'], self.data['score'], self.data['title'],
            self.data['types'], self.data['cover_url'], self.data['release_date'], self.data['regions'],
            self.data['actor_count'], self.data['actors'], self.data['movie_url'], self.data['vote_count'])
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("插入失败")
            print(sql)
            print(self.db.rollback())

    def myclose(self):
        self.db.close()
