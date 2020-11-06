# This file contains project's main helpers functions (format, parsing, clean) 

from w3lib.url import url_query_cleaner
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


def is_recommended(x):
    return True if x == 'Recommended' else False


def format_date(x):

    format_fail = False

    for fmt in ['%b %d, %Y', '%B %d, %Y']:
        try:
            return datetime.strptime(x, fmt).strftime('%Y-%m-%d')
        except ValueError:
            format_fail = True

    for fmt in ['%b %d', '%B %d']:
        try:
            d = datetime.strptime(x, fmt)
            d = d.replace(year=date.today().year)
            return d.strftime('%Y-%m-%d')
        except ValueError:
            format_fail = True

    if format_fail:
        logger.debug(f'Could not process date {x}')

    return x


def parse_float(x:str):
    x = x.replace(',', '')
    try:
        return float(x)
    except:  
        return x


def parse_int(x:str):
    try:
        return int(parse_float(x))
    except: 
        return x


def strip_snr(request):
    url = url_query_cleaner(request.url, ['snr'], remove=True)
    return request.replace(url=url)
