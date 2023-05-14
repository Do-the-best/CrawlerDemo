from DouBan import Spider


if __name__ == '__main__':
    # 构造爬取列表
    urls = \
        ['https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start={}&limit=20'.format(i)
         for i in range(0, 380, 20)]

    spi = Spider(urls)
    movie = spi.get_data()
    for i in range(20 * len(urls)):
        try:
            data = next(movie)
            print(data)
        except:
            print("Finshed")