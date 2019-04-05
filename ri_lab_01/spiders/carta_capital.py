# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class CartaCapitalSpider(scrapy.Spider):
    name = 'carta_capital'
    allowed_domains = ['cartacapital.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(CartaCapitalSpider, self).__init__(*a, **kw)
        with open('seeds/carta_capital.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        urls = [a.attrib['href'] for a in response.css('h3 > a.eltdf-pt-link')]

        for url in urls:
            yield scrapy.Request(url, self.parse_aux)
        #
        # inclua seu código aqui
        #
        #
        #
        #

    def parse_aux(self, response):
        yield {
            'title': response.css('h1.eltdf-title-text::text').get(),
            'section': response.css('div.eltdf-post-info-category > a::text').get(),
            'subtitle': response.css('div.wpb_text_column > div.wpb_wrapper > h3::text').get(),
            'author': response.css('a.eltdf-post-info-author-link::text').get(),
            'text': response.css('div.eltdf-post-text-inner::text').get()
        }
