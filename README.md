# GamesScraping

This repository contains a [Scrapy](https://github.com/scrapy/scrapy) spider for [Steam digital game plattaform](https://steampowered.com) reviews.

## Contributors
| Name | Mail |
| ------ | ------ |
| Carlos Humberto Carreño Díaz | cahucadi@uoc.edu |
| David Barrera Montesdeoca | dbarreram@uoc.edu |

## Installation
First, you will need a Python 3.x+ virtualenv.  

After cloning the repository with
```bash
git clone git@github.com:cahucadi/GamesScraping.git
```


Install Python requirements with:
```bash
pip install -r requirements.txt
```

## Using the crawler

First you need to locate `game_scraping/game_url.txt` file to define the url you want to crawl using [Steam Community page](https://steamcommunity.com/).

This file must have the game url with and id (`APP_ID`) and language (`LANGUAGE`) of the specific review (english, spanish, latam, etc), using the following format:

```bash
https://steamcommunity.com/app/APP_ID/reviews/?browsefilter=mostrecent&snr=1_5_100010_&filterLanguage=LANGUAGE
```

You can initiate the crawl using: 

```bash
scrapy crawl review_spider -o reviews.json
```
Next you can generate a .csv file (semicolon separated) using:

```bash
python main.py
```

`Beware, it can take several hours to proccess`

## APP File description

Most important files:

* `main.py` : used for .csv generation once you get the reviews.json file
* `game_scraping/`
  * `classes.py`: This file contains project's main classes for scrapy item structure from scrapy.Item class
  * `functions.py`: This file contains project's main helpers functions (format, parsing, clean) 
  * `functions.py`: This file contains scrapy default configuration
* `game_scraping/`
  * `review_spider.py`: This file contains project's main spider from scrapy.Spider class
  * `util_functions.py`: This file contains spider needed functions

## DOI File

The dataset is available at Zenodo with DOI:
`10.5281/zenodo.4244834`

And published at:
`http://doi.org/10.5281/zenodo.4244834`
