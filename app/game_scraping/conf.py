# Default configuration

BOT_NAME = 'game_scraping'

JOBDIR = 'temp/reviews'

SPIDER_MODULES = ['game_scraping.spiders']
NEWSPIDER_MODULE = 'game_scraping.spiders'

# We decided to respect robots.txt on website configuration 
ROBOTSTXT_OBEY = True

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0

# Configuration of cache storage
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0 
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [301, 302, 303, 306, 307, 308]
HTTPCACHE_STORAGE = 'game_scraping.classes.CacheStorage'

FEED_EXPORT_ENCODING = 'utf-8'
