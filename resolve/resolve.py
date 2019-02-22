# -*- coding: utf-8 -*-

import MySQLdb
from wordcloud import WordCloud
import matplotlib.pyplot as plt  #绘制图像的模块
import jieba                    #jieba分词
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image


class MyResolve(object):
    def __init__(self):
        print("_____开始运行解析程序_____")

    def connect_data(self):
        conn = MySQLdb.connect('127.0.0.1', 'root', 'mysql', 'test', charset="utf8", use_unicode=True)
        cursor = conn.cursor()
        select_sql = "select * from text"
        cursor.execute(select_sql)
        text = ''
        for data in cursor.fetchall():
            text = text + data[1]
        #统计了爬取多少用户的博文
        select_sql = "select author,count(author)from text group by author having(count(author)>1) ORDER BY count(author) DESC"
        cursor.execute(select_sql)
        i = 0
        for da in cursor.fetchall():
            i += 1
        select_sql = "select count(*) from text"
        re = cursor.execute(select_sql)
        print("爬取到%s条数据" % cursor.fetchone())
        print("爬取了%s位用户" % i)
        print("____开始生成标题词云____")
        self.design(text)

    def design(self, text):
        cut_text = " ".join(jieba.cut(text))
        stopwords = set(STOPWORDS)
        stopwords.add("said")
        path_img = "C://Users/User/Desktop/spiders/bj.png"
        background_image = np.array(Image.open(path_img))
        font = r'C:\Users\User\Desktop\spiders\SimHei.ttf'
        wordcloud = WordCloud(
            font_path=font,
            background_color="white",
            max_font_size=2000,
            # mask参数=图片背景，必须要写上，另外有mask参数再设定宽高是无效的
            mask=background_image).generate(cut_text)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("C://Users/User/Desktop/spiders/cc.png", dpi=300)
        print("文件的路径存储在C://Users/User/Desktop/spiders/cc.png")
        plt.show()



mr = MyResolve()
mr.connect_data()