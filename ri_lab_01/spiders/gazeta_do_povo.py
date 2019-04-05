# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem

import pdb
# scrapy shell ./quotes-mapa.html 
# response.css('.conteudo-mapa a').get()

class GazetaDoPovoSpider(scrapy.Spider):
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = []
    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    def __init__(self, *a, **kw):
        super(GazetaDoPovoSpider, self).__init__(*a, **kw)
        with open('seeds/gazeta_do_povo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        response.css('.linha ').getall()
        

        for elem in response.css('dd'):
            
            title = elem.css('a::attr(title)').get()
            link = elem.css('a::attr(href)').get()

            yield response.follow(link, callback=self.page_parse)
    
    def page_parse(self, response):
        
        session_news = response.css('.coluna1-2')
        for news_item in session_news:
            # pdb.set_trace()
            news_link = news_item.css('article > a::attr(href)').get()
            news_date = news_item.css('article > a::attr(data-publication)').get()
            news_section = news_item.css('article > a::attr(data-section)').get()
            yield response.follow(news_link, callback=self.news_parse)
            
            
        
        

        page = response.url.split("/")[-2]
        filename = 'quotes-posts.txt'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def news_parse(self, response):
        post = response.css('.col-12 height-col')
        dic = {}
        dic['title'] = post.css('.c-title::text').get()
        dic['subtitle'] = post.css('.c-summary::text').get()
        dic['author'] = post.css('.item-name > span::text').get()

        filename = 'rep.txt'
        with open(filename, 'wb') as f:
            f.write(dic)
        return dic



        
        
        #
        #
        #
