# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import scrapy
import re
from crawler.items import QuestionItem
import sqlite3 as lite

from scrapy import signals
from scrapy.mail import MailSender

import logging
import settings

class CrawlerSpider(scrapy.Spider):
    keyword = ''
    name = "crawler"
    start_urls = []
    con = lite.connect('crawler.db',isolation_level=None)
    cur = con.cursor()
    searchPage = True

    def __init__(self, *args, **kwargs):
        super(CrawlerSpider, self).__init__(*args, **kwargs)
        # print 'here'
        # self.keyword = kwargs.get(keyword)
        # print 'here', self.keyword
        self.start_urls.append(settings.URL)
        self.keyword = settings.KEYWORD

        # init logger
        my_handler = logging.FileHandler(u'crawler_log.txt', mode='a', encoding='utf-8', delay=False)
        formatter = logging.Formatter(u'%(asctime)s [%(name)s] %(levelname)s: %(message)s')
        my_handler.setFormatter(formatter)

        my_logger = logging.getLogger(u'CrawlerLogger')
        my_logger.addHandler(my_handler)

    def keywordToUrls(self,keywordStr):
        searchPageUrl = []
        flag = 1
        for word in keywordStr:
            if flag:
                searchPageUrl = 'https://www.quora.com/search?q=' + word
                flag = 0
            else:
                searchPageUrl += '+' + word

        return searchPageUrl

    def parse(self, response):
        #logging and cmd front end
        url = response.url
        print "Crawling " + url
        my_logger = logging.getLogger(u'CrawlerLogger')
        my_logger.info('Crawling %s', url)

        item = QuestionItem()
        item['title'] =response.xpath("//h1/span[2]/text()").extract_first()
        item['link'] = response.url
        description = response.xpath("//div[@class='question_details_text inline_editor_content']/text()").extract_first()
        if description is None:
            item['desc'] = "No description"
        else:
            item['desc'] = description

    	bestContent = response.css('.ExpandedAnswer').extract_first()
    	if bestContent is None:
    		item['bestContent'] = "No best content"
    	else:
    		item['bestContent'] = bestContent

    	bestView = response.xpath("//div[@class='CredibilityFact']/text()[1]").extract()
        if bestView is None or len(bestView)==0:
            item['bestView'] = 0
        else:
            bestViewSplit = bestView[0].split(' ')

            if 'k' in bestViewSplit[0]:
                view  = bestViewSplit[0][0:len(bestViewSplit[0])-1]
                viewNum = float(view) * 1000
            else:
                viewNum = float(bestViewSplit[0])

           	item['bestView']= viewNum

        item['bestVote'] = 0
        item['keyword'] = self.keyword
        yield item

        for href in response.css(".related_question a::attr('href')"):
            url = response.urljoin(href.extract())
            self.cur.execute("SELECT count(Id) from RequestUrls where requestUrl=(?);",(url,))
            if(self.cur.fetchone()[0] <= 0):
                self.cur.execute("INSERT INTO RequestUrls(requestUrl) VALUES(?)",(url,))
                try:
                    request = self.make_requests_from_url(url)
                    request.meta['keyword'] = self.keyword
                    yield request
                except:
                    print "catch yield error"
                    my_logger.error("catch yeild error")
                    continue

    def follow_robot(self, url):
        for n,line in enumerate(open("robot.txt")):
            if n+1 in [1088,]:
                if(line.find('Disallow:')):
                    p = line.find('Disallow:')
                    s = line[p+10,]
                    pattern = re.compile(s)
                    if (pattern.match(url)):
                        return False
        return True

    #spider closed signal
    @classmethod
    def from_crawler(cls, crawler):
        spider = cls()
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    #spider closed, send email
    def spider_closed(self, spider):
        mailer = MailSender(mailfrom="11601F15Team14@gmail.com",smtphost="smtp.gmail.com",smtpport=587,smtpuser="11601F15Team14@gmail.com",smtppass="team14gmail")

        # get statistics
        self.cur.execute("SELECT COUNT(*) FROM Results")
        crawled = self.cur.fetchone()

        self.cur.execute("SELECT COUNT(*) FROM RequestUrls")
        totalUrl = self.cur.fetchone()
        toBeCrawled = totalUrl[0] - crawled[0]

        emailBody = "Crawled: " + str(crawled[0]) + "\nTo be crawled: " + \
                    str(toBeCrawled) + "\nProgress: " + str(float(crawled[0])/totalUrl[0])

        return mailer.send(to=["11601F15Team14@gmail.com"],subject="Test",body=emailBody)
