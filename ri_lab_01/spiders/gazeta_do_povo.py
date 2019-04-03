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

    def __init__(self, *a, **kw):
        super(GazetaDoPovoSpider, self).__init__(*a, **kw)
        with open('frontier/gazetadopovo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):

        LINKS_SELECTOR = 'div.conteudo-mapa a::attr(href)'
            
        #self.start_urls = brickset.css(LINKS_SELECTOR).getall(),
        #self.start_urls = [str(url) for url in self.start_urls]
        
        #for url in self.start_urls:
        #    scrapy.Request(url)   
        
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        #
        #
        #
