# This file contains spider's most used functions

import re

from ..functions import parse_int
from ..classes import Review, ReviewLoader
from w3lib.url import url_query_parameter

# Select and load on a scrapy item the content on HTML tags
def generate_review(review, product_id, product_name, page=1, order=None):

    loader = ReviewLoader(Review(), review)

    loader.add_value('product_id', product_id)
    loader.add_value('product_name', product_name)
    loader.add_value('page', page)
    loader.add_value('page_order', order)

    loader.add_css('recommended', '.title::text')
    loader.add_css('date', '.date_posted::text', re='Posted: (.+)')
    loader.add_css('text', '.apphub_CardTextContent::text')
    loader.add_css('hours', '.hours::text', re='(.+) hrs')
    loader.add_css('comment_count', '.apphub_CardCommentCount::text')

    loader.add_css('user_id', '.apphub_CardContentAuthorName a::attr(href)', re='.*/profiles/(.+)/')
    loader.add_css('username', '.apphub_CardContentAuthorName a::text')
    loader.add_css('products', '.apphub_CardContentMoreLink ::text', re='([\\d,]+) product')

    feedback = loader.get_css('.found_helpful ::text')
    loader.add_value('found_helpful', feedback, re='([\\d,]+).*helpful')
    loader.add_value('found_unhelpful', feedback, re='([\\d,]+).*unhelpful')
    loader.add_value('found_funny', feedback, re='([\\d,]+).*funny')

    early_access = loader.get_css('.early_access_review')

    if early_access:
        loader.add_value('early_access', True)
    else:
        loader.add_value('early_access', False)

    return loader.load_item()


# function used to manipulate page count
def get_page_number(response):
    from_page = response.meta.get('from_page', None)

    if from_page:
        page = from_page + 1
    else:
        page = url_query_parameter(response.url, 'p', None)
        if page:
            page = parse_int(page)

    return page

# function create to get product id from request url
def get_product_id(response):
    product_id = response.meta.get('product_id', None)

    if not product_id:
        try:
            return re.findall("app/(.+?)/", response.url)[0]
        except: 
            return None
    else:
        return product_id
