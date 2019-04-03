# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


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
        print(response.css('div.conteudo-mapa'))
        print("ooooooooooooooooooooooooooooooooooooooooooooooooooo")
        SET_SELECTOR = 'div.conteudo-mapa'
        for brickset in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'dt ::text'
            IMAGE_SELECTOR = 'a ::attr(href)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }
        
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        #
        #
        #
