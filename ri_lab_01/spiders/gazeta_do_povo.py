# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


def get_selector(name):
    selectors = {
        "page_section": ['div.box-mapa a::attr(href)'],
        "news": ['section.tpl-editoria-lista article.c-chamada a::attr(href)', 'article.c-chamada a::attr(href)'],
        
        "content": ['article.post', 'div#post', 'article.gp-cont'],
        "title": ['h1.c-title::text', 'h1.title-02::text', 'h1.c-titulo::text'],
        "subtitle": ['h2.c-summary::text', 'h2.c-sumario::text', 'h3.title-03::text'],
        "section": ['ul.c-section-header li.c-title-content a::text', 'h2.titulo a::text', 'header div.c-overhead span::text'],
        "author": ['div.c-credits ul li:first-child::text', 'div.c-credits ul li:first-child span::text', 'div.c-creditos ul li:first-child span::text', 'header h3.c-sobretitulo span::text', 'section#post span.autor-creditos::text', 'ul.c-creditos a::attr(title)'],
        "date": ['div.c-credits li:last-of-type::text', 'div.c-creditos li.data-publicacao time::text', 'section#post span.data-hora::text', 'ul.c-creditos time::text'],
        "text": ['div.c-content p::text', 'article.texto-post p::text', 'article.texto-post p::text'],
    }
    return selectors[name]

def query(container, selector):
    if container is None:
        return

    for css_selector in get_selector(selector):
        tag = container.css(css_selector)
        if tag.get() is not None:
            return tag


class GazetaDoPovoSpider(scrapy.Spider):
    name = 'gazeta_do_povo'
    allowed_domains = ['gazetadopovo.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(GazetaDoPovoSpider, self).__init__(*a, **kw)
        with open('seeds/gazeta_do_povo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())
        self.start_urls[0] += 'mapa/'


    def parse(self, response):
        """Get links to the sections"""
        for section_url in query(response, 'page_section').getall():
            if section_url is not None:
                section_url = response.urljoin(section_url) if section_url.startswith('/') else section_url
                yield scrapy.Request(section_url, callback=self.get_news_pages)
        
        self.write_page(response)


    def get_news_pages(self, response):
        """Get all links to news pages"""
        news = query(response, 'news')
        if news is None:
            return

        for news_url in news.getall():
            if news_url is not None:
                news_url = response.urljoin(news_url) if news_url.startswith('/') else news_url
                yield scrapy.Request(news_url, callback=self.get_data)

        self.write_page(response)


    def get_data(self, response):
        """Get the data from a news page"""
        get_value = lambda tag: tag.get() if tag else tag
        get_values = lambda tag: tag.getall() if tag else tag

        content = query(response, 'content')
        section = query(content, 'section')
        title = query(content, 'title')
        subtitle = query(content, 'subtitle') 
        author = query(content, 'author')
        date = query(content, 'date')
        text = query(content, 'text')

        yield {
            "url": response.url,
            "secao": get_value(section),
            "titulo": get_value(title),
            "subtitulo": get_value(subtitle),
            "autor": get_value(author),
            "data": get_value(date),
            "texto": get_values(text),
        }

        self.write_page(response)
        

    def write_page(self, response):
        page = response.url.split(".")[1]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
