# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem

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
        parcial = []
        NEWS_LINK = 'loc::text'
        # <loc> do sitemap
        for link in response.css(NEWS_LINK).getall():
            yield response.follow(link, self.parse)
            # noticias por dia
            for day_news in response.css(NEWS_LINK).getall():
                yield response.follow(day_news, self.parse)

                for news in response.css(NEWS_LINK).getall():
                    answer = response.follow(news, self.parse)
                    parcial.append(
                        {
                            'title':answer.css('h1::text').get(),
                            'link': day_news, 
                            'session': answer.css("c-title-content").get(),
                            'date': answer.css("c-credits mobile-hide").get(), 
                            'text': answer.css("c-credits mobile-hide").get("paywall-google")
                            }
                        )
        
        filename = 'parcial.html' 
        with open(filename, 'w') as f:
            for item in parcial:
                print >> filename, item
        # LINKS_SELECTOR = 'div.loc a'
            
        # self.start_urls = brickset.css(LINKS_SELECTOR).getall(),
        # self.start_urls = [str(url) for url in self.start_urls]
        # print(self.start_urls) 
        #for url in self.start_urls:
        #    scrapy.Request(url)   
        
        # page = response.url.split("/")[-2]
        # filename = 'quotes-teste-original.html' 
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        #
        #
        #
