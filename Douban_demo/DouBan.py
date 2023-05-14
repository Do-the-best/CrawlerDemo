# -*- coding: UTF-8 -*-
# @Author: Mr. Li
# @Date: 2023/5/14 12:28

"""
剧情：https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action=
喜剧：https://movie.douban.com/typerank?type_name=%E5%96%9C%E5%89%A7&type=24&interval_id=100:90&action=
动作：https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20
"""

import json
import urllib.request


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
                    data['rank'] = movie['rank']  # 排名
                    data['score'] = movie['score']  # 评分
                    data['title'] = movie['title']  # 电影名
                    data['types'] = ', '.join(movie['types'])  # 类型
                    data['cover_url'] = movie['cover_url']  # 海报
                    data['release_date'] = movie['release_date']  # 上映时间
                    data['regions'] = ', '.join(movie['regions'])  # 地区
                    data['actor_count'] = movie['actor_count']  # 主演数量
                    data['actors'] = ', '.join(movie['actors'])  # 演员列表
                    data['movie_url'] = movie['url']  # 详情页链接
                    data['vote_count'] = movie['vote_count']  # 评价人数
                except:
                    pass
                yield data
