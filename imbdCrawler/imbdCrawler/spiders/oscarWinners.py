# -*- coding: utf-8 -*-
import scrapy
import re
import socket
import datetime
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
    Genres_out = Join("")

    Length_in = MapCompose(int)
    Length_out = TakeFirst()

    

    Directors_in = MapCompose(
            str.strip, 
            lambda x:x.replace("\n",""), 
            lambda x:x.split("|")[0], 
            lambda x:x.split(":")[1],
            str.strip
            )
    Directors_out = Join("")


    Actors_in = MapCompose(
            str.strip, 
            lambda x:x.replace("\n",""), 
            lambda x:x.split("|")[1], 
            lambda x:x.split(":")[1],
            str.strip
            )
    Actors_out = Join("")


    Rating_in = MapCompose(float)
    Rating_out = TakeFirst()


    Votes_in = MapCompose(lambda i:i.replace(",",""),int)
    Votes_out = TakeFirst()

    Income_in = MapCompose(lambda i:i.replace(",",""),float)
    Income_out = TakeFirst()

    #page_in = MapCompose(lambda i:urljoin(response.url,i))
    Page_out = Join("")


    Url_out = Join("")

    Server_out = Join("")

    Date_out = Join("")

    Project_out = Join("")

    Spider_out = Join("")

class OscarwinnersSpider(scrapy.Spider):
    name = 'oscarWinners'
    allowed_domains = ['http://www.imdb.com/search/title?count=100']
    start_urls = ['http://www.imdb.com/search/title?count=100&groups=oscar_best_picture_winners&sort=year,desc&view=advanced&ref_=nv_ch_osc_2']

    def parse(self, response):
        movies = response.xpath('//*[@class="lister-item-content"]')
        self.log("Movies found : {}".format(len(movies)))
        for movie in movies:
            loader = MovieLoader(item=ImbdcrawlerItem(), selector=movie)

            loader.add_xpath('Title','*[@class="lister-item-header"]/a/text()')
            loader.add_xpath('Year','*[@class="lister-item-header"]//*[contains(@class,"lister-item-year")]/text()', re='\d{4}')
            loader.add_xpath('Description','*[@class="text-muted"]/text()')
            loader.add_xpath('Genres','*[contains(@class,"text-muted")]/*[@class="genre"]/text()')
            loader.add_xpath('Length','*[contains(@class,"text-muted")]/*[@class="runtime"]/text()',re='\d{2,3}')
            loader.add_xpath('Directors','*[@class=""]//text()', Join(""))
            loader.add_xpath('Actors','*[@class=""]//text()', Join(""))
            loader.add_xpath('Rating','.//*[contains(@class,"ratings-imdb-rating")]/@data-value')
            loader.add_xpath('Votes','*[@class="sort-num_votes-visible"]/*[@name="nv"][1]/@data-value')
            loader.add_xpath('Income','*[@class="sort-num_votes-visible"]/*[@name="nv"][2]/@data-value')
            loader.add_xpath('Page','*[@class="lister-item-header"]/a/@href', MapCompose(lambda i:urljoin(response.url,i)))
            

            loader.add_value('Url',response.url)
            loader.add_value('Project', self.settings.get('BOT_NAME'))
            loader.add_value('Spider',self.name)
            loader.add_value('Server',socket.gethostname())
            loader.add_value('Date',str(datetime.datetime.now()))
            yield loader.load_item()


