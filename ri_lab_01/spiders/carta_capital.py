# -*- coding: utf-8 -*-
import scrapy
import json

from datetime import datetime

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class CartaCapitalSpider(scrapy.Spider):
    name = 'carta_capital'
    allowed_domains = ['cartacapital.com.br']
    start_urls = []
    visited_urls = []

    def __init__(self, *a, **kw):
        super(CartaCapitalSpider, self).__init__(*a, **kw)
        with open('seeds/carta_capital.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def isValidCartaCapitalLink(self, link):
        for section in self.start_urls:
            if (section.lower() in link.lower()):
                return True
        return False

    def isValidNews(self, link):
        if (self.isValidCartaCapitalLink(link) and (self.visited_urls.count(link) == 0) and (link is not None)):
            return True
        return False

    def parse(self, response):
        urls = [a.attrib['href'] for a in response.css('h3 > a.eltdf-pt-link')]

        for url in urls:
            yield scrapy.Request(url, self.parse_aux)

        for next in response.css('a::attr(href)').getall():
            if (self.isValidNews(next)):
                yield scrapy.Request(next, self.parse)
            self.urls.append(next)

    def parse_aux(self, response):
        if (int(response.css('div.eltdf-post-info-date a::attr(href)').get().split("/")[-3]) >= 2018):
            yield {
                'title': response.css('h1.eltdf-title-text::text').get(),
                'sub_title': response.css('div.wpb_text_column > div.wpb_wrapper > h3::text').get(),
                'author': response.css('a.eltdf-post-info-author-link::text').get(),
                'date': datetime.strptime(response.xpath("//meta[@property='article:published_time']/@content").get().replace("T", " ").split("+")[0], '%Y-%m-%d %H:%M:%S'),
                'section': response.css('div.eltdf-post-info-category > a::text').get(),
                'text': "".join(response.css('article p::text').getall()),
                'url': response.url
            }
