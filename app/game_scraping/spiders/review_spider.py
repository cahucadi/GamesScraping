# Proyect main spider

import scrapy
from scrapy.http import FormRequest, Request
from os import path

from .util_functions import generate_review, get_page_number, get_product_id

class ReviewSpider(scrapy.Spider):
    
    name = 'review_spider'

    product_name = ''
    
    # game_review_url storages a list of urls to analyze defined in game_url.txt
    # for now, only works with ONE URL, because it present some bugs on game title for multiple url
    game_review_url = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "..", "game_url.txt"))
        f = open(filepath, "r")

        content = []
        content = f.readlines()
        
        self.game_review_url = [x.strip() for x in content] 


    def start_requests(self):
        for url in self.game_review_url:
                yield Request(url, callback=self.parse_game_review)


    def parse_game_review(self, response):
        
        page = get_page_number(response)
        product_id = get_product_id(response)

        if(self.product_name == ''):
            self.product_name = response.css('div .apphub_AppName ::text').extract()
        
        # extract reviews on current page
        reviews = response.css('div .apphub_Card')

        if(page==None or page==0):
            page = 1

        # for every item list of reviews, generates on Review scrapy item
        for i, review in enumerate(reviews):
            yield generate_review(review, product_id, self.product_name, page, i)

        # it need to load more reviews, otherwise it stops on first page
        form = response.xpath('//form[contains(@id, "MoreContentForm")]')
        if form:
            yield self.process_pagination_form(form, page, product_id, self.product_name)


    # function defined for processing multiple page requests
    def process_pagination_form(self, form, page=1, product_id=None, product_name=None):
        action = form.xpath('@action').extract_first()
        names = form.xpath('input/@name').extract()
        values = form.xpath('input/@value').extract()

        formdata = dict(zip(names, values))
        meta = dict(prev_page=page, product_id=product_id)

        return FormRequest(
            url=action,
            method='GET',
            formdata=formdata,
            callback=self.parse_game_review,
            meta=meta
        )