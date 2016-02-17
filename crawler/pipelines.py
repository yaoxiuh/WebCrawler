import sqlite3 as lite
import sys


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):
    def __init__(self):
        con = lite.connect('crawler.db')

        with con:

            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Results(Id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "Keyword TEXT, Title TEXT, Link TEXT, Description TEXT, BestContent TEXT, BestVote INTEGER, BestView INTEGER)")


    def process_item(self, item, spider):
        con = lite.connect('crawler.db')
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO Results (Keyword, Title, Link, Description, BestContent, BestVote, BestView) " \
                         "VALUES (?,?,?,?,?,?,?)", (item['keyword'], item['title'], item['link'], item['desc'], item['bestContent'], item['bestVote'], item['bestView']))

        return item
