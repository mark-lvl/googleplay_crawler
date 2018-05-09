# googleplay_crawler
This crawler was written in Python by [Scrapy](https://scrapy.org/) framework in order to scrape content of Android applications which
are published in [Google Play](https://play.google.com/store/apps) store.

You can deploy it on [ScrapingHub](scrapinghub.com) or easily set a daemon in your personal machine by [scrapyd](https://github.com/scrapy/scrapyd)
and start to scraping items.

## How to Run
First, make sure you are in project directory and then easily run the crawler by following command:

```bash
scrapy crawl gapps -o OUTPUTFILENAME.EXT
```
For example, if you're going to export your data in `csv` format in your current directory, you can run:
```bash
scrapy crawl gapps -o apps_data.csv
```

#### Note
This repository is under development. 
Upcoming features:
 - Implementing tags support in order to toggle fields in output
 - Configuring AutoThrottle feature
 - Setting USER-AGENT and corresponding settings
