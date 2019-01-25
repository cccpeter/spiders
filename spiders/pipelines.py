# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import json

class SpidersPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):

    def process_item(self, item, spider):
        # print('开始插入数据库_____________________________')
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'mysql', 'test', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        item['link'] = json.dumps(item['link'])
        insert_sql = "insert into text(id,title,link)VALUE ('','%s','%s')" % (item['title'], item['link'])
        # print('sql语句：%s'% insert_sql)
        self.cursor.execute(insert_sql)
        self.conn.commit()
        self.conn.close()

    # def process_item(self,item,spider):
    #     insert_sql="""
    #     insert into text('',text)VALUE (%s,%s)
    #     """
    #     self.cursor.execute(insert_sql,(item['id'],item['text']))
    #     self.conn.commit()