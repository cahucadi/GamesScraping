# This file contains project's main classes

import logging
import os

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, Join, MapCompose, TakeFirst
from scrapy.utils.request import request_fingerprint
from scrapy.extensions.httpcache import FilesystemCacheStorage

from .functions import parse_int, parse_float, format_date, is_recommended, strip_snr


# Class for cleaning HTML white spaces, tabs and end of lines 
class CleanSpaces:
    def __init__(self, chars=' \r\t\n'):
        self.chars = chars

    def __call__(self, value):
        try:
            return value.strip(self.chars)
        except: 
            return value

# Scrapy item class for reviews, it defines the fields to be extracted
class Review(scrapy.Item):
    
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    page = scrapy.Field()
    page_order = scrapy.Field()

    recommended = scrapy.Field(
        output_processor=Compose(TakeFirst(), is_recommended),
    )
    date = scrapy.Field(
        output_processor=Compose(TakeFirst(), format_date)
    )
    text = scrapy.Field(
        input_processor=MapCompose(CleanSpaces()),
        output_processor=Compose(Join('\t'), CleanSpaces())
    )
    hours = scrapy.Field(
        output_processor=Compose(TakeFirst(), parse_float)
    )
    found_helpful = scrapy.Field(
        output_processor=Compose(TakeFirst(), parse_int)
    )
    found_unhelpful = scrapy.Field(
        output_processor=Compose(TakeFirst(), parse_int)
    )
    found_funny = scrapy.Field(
        output_processor=Compose(TakeFirst(), parse_int)
    )
    comment_count = scrapy.Field(
        output_processor=Compose(TakeFirst(), parse_int)
    )
    username = scrapy.Field()

    user_id = scrapy.Field()
    products = scrapy.Field(
        output_processor=Compose(TakeFirst(), parse_int)
    )
    early_access = scrapy.Field()

# From Scrapy documentation, provide a convenient mechanism for populating scraped items
# https://docs.scrapy.org/en/latest/topics/loaders.html
class ReviewLoader(ItemLoader):
    default_output_processor = TakeFirst()

# Cache storage class in temp/reviews folder
class CacheStorage(FilesystemCacheStorage):
    def _get_request_path(self, spider, request):
        request = strip_snr(request)
        key = request_fingerprint(request)
        return os.path.join(self.cachedir, spider.name, key[0:2], key)