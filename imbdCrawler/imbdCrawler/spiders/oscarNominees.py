# -*- coding: utf-8 -*-
import scrapy
import re
import socket
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from imbdCrawler.items import ImbdcrawlerItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from urllib.parse import urljoin


class MovieLoader(ItemLoader):

    Title_in = MapCompose(str.strip, str.title)
    Title_out = Join("")

    Description_in = MapCompose(str.strip, lambda x:x.replace("\n"," "), lambda x:x.replace(";",","))
    Description_out = Join("")

    Year_in = MapCompose(int)
    Year_out = TakeFirst()

    Genres_in = MapCompose(str.strip)
    Genres_out = Join(",")

    Length_in = MapCompose(int)
    Length_out = TakeFirst()



    Directors_in = MapCompose(str.strip)
    Directors_out = Join(",")



    Actors_in = MapCompose(str.strip)
    Actors_out = Join(",")

    Rating_in = MapCompose(str.strip,float)
    Rating_out = TakeFirst()


    Votes_in = MapCompose(str.strip,lambda i:i.replace(",",""),int)
    Votes_out = TakeFirst()

    Income_in = MapCompose(lambda i:i.replace(",",""),float)
    Income_out = TakeFirst()


    Budget_in = MapCompose(lambda i:i.replace(",",""),float)
    Budget_out = TakeFirst()
    
    Url_out = Join("")

    Server_out = Join("")

    Date_out = Join("")

    Project_out = Join("")

    Spider_out = Join("")

class OscarnomineesSpider(CrawlSpider):
    name = 'oscarNominees'
    start_urls = ['http://www.imdb.com/list/ls057163321/?start=1&view=detail&sort=release_date_us:desc']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=r'//*[@class="pagination"]')),
        Rule(LinkExtractor(restrict_xpaths=r'//*[contains(@class,"list_item")]/*[@class="info"]/b'), callback='parse_item')
    )

    def parse_item(self, response):
        loader = MovieLoader(item=ImbdcrawlerItem(), response=response)
        loader.add_xpath('Title','//*[@class="title_wrapper"]/*[@itemprop="name"]/text()')
        loader.add_xpath('Year','//*[@id="titleYear"]//text()', re='\d{4}')
        loader.add_xpath('Description','//*[@itemprop="description"]/text()')
        loader.add_xpath('Genres','//*[@itemprop="genre"]/text()',re=r'[a-zA-Z]+')
        loader.add_xpath('Length','//*[@class="txt-block"]/*[@itemprop="duration"]/text()',re='\d{2,3}')
        loader.add_xpath('Directors','//*[@itemprop="director"]//*[@itemprop="name"]/text()')
        loader.add_xpath('Actors','//*[@itemprop="actors"]//*[@itemprop="name"]/text()')
        loader.add_xpath('Rating','//*[@itemprop="ratingValue"]/text()')
        loader.add_xpath('Votes','//*[@itemprop="ratingCount"]/text()')
        loader.add_xpath('Income','//*[contains(text(),"Gross:")]/parent::div/text()', re='[\d,]+')
        loader.add_xpath('Budget','//*[contains(text(),"Budget:")]/parent::div/text()', re='[\d,]+')


        loader.add_value('Url',response.url)
        loader.add_value('Project', self.settings.get('BOT_NAME'))
        loader.add_value('Spider',self.name)
        loader.add_value('Server',socket.gethostname())
        loader.add_value('Date',str(datetime.datetime.now()))
        yield loader.load_item()
