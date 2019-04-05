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
        selectors = self.get_selectors('en')
        is_home_page = response.url == self.start_urls[0]

        if not is_home_page:
            section = response.css(selectors['content'])
            
            yield {
                "url": response.url,
                "secao": section.css(selectors['section']).get(),
                "titulo": section.css(selectors['title']).get(),
                "autor": section.css(selectors['author']).get(),
                "data": section.css(selectors['date']).get(),
                "texto": section.css(selectors['text']).getall(),
                "subtitulo": "inexistente",
            }

        for next_url in response.css(selectors['article']).getall():
            if next_url is not None:
                yield scrapy.Request(next_url, callback=self.parse)


        page = response.url.split(".")[1]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


    def get_selectors(self, type):
        article_selector = 'section:not(.bloco-opiniao) article.c-chamada.com-img:not(.c-live) a::attr(href)'

        if type == 'pt':
            return {
                "article": article_selector,
                "content": "section.bl-post",
                "title": 'h1.c-titulo::text',
                "author": 'ul.c-creditos a::attr(title)',
                "date": 'ul.c-creditos time::text',
                "text": 'article.texto-post p::text'
            }
        else:
            return {
                "article": article_selector,
                "content": 'article.post',
                "title": 'h1.c-title::text',
                "author": 'div.c-credits li.item-name span::text',
                "date": 'div.c-credits li:last-of-type::text',
                "text": 'div.c-content p::text',
                "section": 'ul.c-section-header li.c-title-content a::text'
            }