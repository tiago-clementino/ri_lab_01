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
        with open('seeds/gazeta_do_povo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        for section in response.css('section.bl-post'):
            yield {
                "title": section.css('h1.c-titulo::text').get(),
                "subtitulo": "",
                "autor": section.css('ul.c-creditos a::attr(title)').get(),
                "data": section.css('ul.c-creditos time::text').get(),
                "secao": "",
                "texto": section.css('article.texto-post p::text').getall()[0],
                "url": response.url
            }

        for next_url in response.css('article.c-chamada a::attr(href)').getall():
            if next_url is not None:
                yield scrapy.Request(next_url, callback=self.parse)


        page = response.url.split(".")[1]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

