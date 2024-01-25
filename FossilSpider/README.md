# Web spider for finding fossil ties

# 🕷️

**Author and maintainer**: 
Aaron Pereira, Solid Sustainability Research

**Contact**: aaron@solid-sustainability.org
  
**Repo**: https://bitbucket.org/aaronpereirarobotics/fossil-spider

## About the spider

This spider:

1) searches through a website (e.g. a university website)
2) Looks for search terms such as "Shell" and "Aramco" on each page
3) Saves the URL of pages on which one of these search terms are found in a spreadsheet (CSV format) along with the context in which they were found. You can then look at the spreadsheet and check out any links you find interesting.


## Getting started


You will need:

- Python 3 (tested with version 3.10.6 - check your version by executing `python3 --version` in your terminal)
- `pip`, in case not already installed with Python (tested with version 22.0.2 - you can install it on Linux with `sudo apt-get install pip`. On Windows it should come pre-installed with Python.)
- `scrapy` (tested with version 2.9.0 - you can install it with `pip install scrapy`)
- `beautifulsoup4` (tested with version 4.11.1 - you can install it with `pip install beautifulsoup4`)

This repo is made and tested in Ubuntu 22.04.1, but should work in other operating systems as well. 


## Running the spider

1. Open `fossilbot/spiders/crawlSpider.py` and go to line 10,  

2. Enter:

  a. the website you want to search, under `allowed_domains`, ignoring `/` and `https://www.`  

  b. the URL you want to start from, under `start_urls`

  c. *optional*: Enter any URLs you want to ignore, under `deny_urls`, as a list of regular expressions
	
  d. the search terms, under `search_for_list`, as a list of regular expressions  

3. Go to your terminal and navigate to the directory of the `crawlSpider.py` 

4. Run `scrapy runspider crawlSpider.py`

5. If you need to stop the spider, just press `Ctrl+C` in the terminal, once, otherwise wait until the spider is finished

6. Look at the output (the generated CSV spreadsheet in the folder `fossilbot/output`)

7. If something isn't quite right, check the log in `fossilbot/spiders/logs`. Be aware - each run of the spider overwrites the previous log! You can change this, see below.

## Advanced

- **Starting point**: you don't have to start (`start_urls`) at the main page of the website.

- **Ignore certain links**: is there a huge, irrelevant portion of your website? Add it to the deny list (`deny_urls`).

- **Limit the depth of the search**: the depth is the maximum number of links that the search can follow starting from the `start_urls`. Currently this is set to 10. You can change or remove this limit:
	+ Open the file `fossilbot/settings.py`
	+ Change the limit on line 107, or put a `#` before the line to ignore the depth limit. 
	
- **Speed it up**. You can remove the delay:
	+ Open the file `fossilbot/settings.py`
	+ Go to line 28 and comment out the line (add a `#` before it.
	
	Of course, this will will increase the traffic on the website, and there's a chance (unlikely) they might ban your spider (see below).
	
	You can also add more URLs to the deny list or focus only on portions of the website that you know might contain ties (see above).
	
- **Append don't overwrite logs**: Currently, the log of the most recent crawl overwrites the log of the crawl before that. This is so that you don't have to keep deleting your log files (they get very big). If you don't want that:
	+ Open the file `fossilbot/settings.py`
	+ Go to line 97 and change `False` to `True`.
	
	The new log will be appended to the old log. Be aware that this log file will grow big very fast! 

- **Option to ignore `robots.txt`**: The file `robots.txt` is often found after the domain name (e.g. `www.tudelft.nl/robots.txt`). It tells web crawlers what parts of the website they should and should not look at, and it's usually to help us out (i.e. so that we can ignore parts of the website that are outdated or just full of formatting). For that reason, the default is to respect the rules in `robots.txt`. 

	Of course, it's not illegal to ignore it. If you have looked at the `robots.txt` file of the website you are searching and suspect that there might be interesting information in the excluded parts of the website, you can:
	+ Open the file `fossilbot/settings.py`
	+ Change line 20 to `ROBOTSTXT_OBEY = False`
	
- **Disabling cookies**. Cookies are enabled by default. If you don't want that:
	+ Open the file `fossilbot/settings.py`
	+ Uncomment (remove the `'#'` at the beginning of) line 34
	
- **Avoid getting banned**. Bots are annoying for websites because they request a lot of traffic, and you could end up getting banned from the website. To avoid this, see [Scrapy's guide to not getting banned](https://docs.scrapy.org/en/latest/topics/practices.html#bans). You could increase the download delay to between 2 and 3:
	+ Open the file `fossilbot/settings.py`
	+ Go to line 28 and change the delay to your desired value.
	
	Of course, this will make your bot run slower. You could always run it overnight.	
	
	
## Legality

The spider(s) in this repo:  

- only access publicly available data,  

- do not attempt to bypass firewalls,  

- do not explicitly collect personal data (the "context" field of the spider's results collects a little text before and after the incidence of the keyword in the text body, to help understand the context in which the keyword is found. It can be that this contains a name or an email, but this is unlikely and not the purpose of the spider. The "context" field is deliberately limited to only few characters around the keyword for this reason),  

- the results of the web crawl are not to be used for commercial purposes.

As such (to the best of our knowledge) the use of these spiders in the ways described in this readme is legal. See e.g. [this article](https://research.aimultiple.com/web-scraping-ethics/).