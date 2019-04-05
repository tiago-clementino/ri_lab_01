# -*- coding: utf-8 -*-
import json
import pdb

import scrapy
import pandas

from ri_lab_01.items import ArticleItem
from ri_lab_01.items import ArticleCommentItem



def parse_article(response):
    
    item = ArticleItem()
    item['url'] = response.request.url
    item["section"] = response.css("div.seccion-migas span span::text").get()
    item["title"] = response.css("h1::text").get()
    item["subtitle"] = response.css("h2::text").get()
    item["date"] = response.css("time::attr(datetime)").get()
    item["author"] = response.css("span.autor-nombre a::text").get()
    item["text"] = locate_text(response)

    return item 

def locate_text(response):
   text = '' 
   p_res = response.css("div.articulo-cuerpo p::text").getall()
   p_res_text = ''.join(p_res) 

   span_res = response.css("div.articulo-cuerpo span::text").getall()
   span_res_text = ''.join(span_res) 
   
   galeria_res = response.css("div.articulo-galeria figcaption \
                              span.foto-texto::text").getall()
   galeria_res_text = ''.join(galeria_res)

   if len(p_res_text) >= len(span_res_text) and \
      len(p_res_text) >= len(galeria_res_text):
        text = p_res
   
   elif len(span_res_text) >= len(p_res_text) and \
      len(span_res_text) >= len(galeria_res_text):
        text = span_res

   else:
        text = galeria_res
   
   return text


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('seeds/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        articles = response.css("div.articulo__interior")
     
        for article in articles:
            url = article.css("h2.articulo-titulo a::attr(href)").get()
            if url :
                url = "https:" + url 
                yield response.follow(url, callback=parse_article)
   

