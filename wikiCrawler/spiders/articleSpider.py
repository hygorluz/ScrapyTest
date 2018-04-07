import unicodedata
from pprint import pprint

from pymongo import MongoClient
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from wikiCrawler.items import Article


class ArticleSpider(CrawlSpider):
    name = 'article'
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [
        "https://en.wikipedia.org/wiki/Python_(programming_language)"]
    rules = [Rule(LinkExtractor(allow=('(/wiki/)((?!:).)*$')),
                  callback="parse_item", follow=True)]
    
    client = MongoClient(port=27017)
    db = client.wikicrawldb


    def parse_item(self, response):
        item = Article()
        title = response.xpath('//h1/text()')[0].extract()
        subtitles = response.xpath(
            '//div[@class="toc"]//li/a/span[@class="toctext"]/text()').extract()
        content = response.xpath(
            '//div[@class="mw-parser-output"]/*[not(self::table)][not(self::div)]//text()').extract()
        pprint("Title is: " + title)
        pprint("Subtitles : " + str(subtitles))
        pprint("content is: " + str(content))
        content_string = unicodedata.normalize("NFKD", "".join(content))
        
        item['title'] = title
        item['subtitles'] = subtitles
        item['content'] = content_string.replace(
            '"', "").replace('\\n', '\n').replace('\\u00a0', ' ')
        result=db.reviews.insert_one(business)
        print('Created {0} of 100 as {1}'.format(x,result.inserted_id))
        return item
