# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SpidersPipeline(object):
    def process_item(self, item, spider):
        return item
import MySQLdb
from twisted.enterprise import adbapi
class MysqlPipeline(object):
    def __init__(self,item,spider):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'cpd954553107', 'test', charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        insert_sql="""
        insert into text('',text)VALUE (%s,%s)
        """
        self.cursor.execute(insert_sql,(item['id'],item['text']))
        self.conn.commit()