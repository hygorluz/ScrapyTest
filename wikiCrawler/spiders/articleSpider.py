from scrapy.contrib.spiders import CrawlSpider, Rule
from wikiCrawler.items import Article
from scrapy.linkextractors import LinkExtractor

import unicodedata


class ArticleSpider(CrawlSpider):
    name = 'article'
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [
        "https://en.wikipedia.org/wiki/Python_(programming_language)"]
    rules = [Rule(LinkExtractor(allow=('(/wiki/)((?!:).)*$')),
                  callback="parse_item", follow=True)]

    def parse_item(self, response):
        item = Article()
        title = response.xpath('//h1/text()')[0].extract()
        subtitles = response.xpath(
            '//div[@class="toc"]/ul/li/a/span[@class="toctext"]/text()').extract()
        content = response.xpath(
            '//div[@class="mw-parser-output"]/*[not(self::table)][not(self::div)]//text()').extract()
        print("Title is: " + title)
        print("Subtitles : " + str(subtitles))
        print("content is: " + str(content))
        content_string = unicodedata.normalize("NFKD", "".join(content))
        
        item['title'] = title
        item['subtitles'] = subtitles
        item['content'] = content_string.replace(
            '"', "").replace('\\n', '\n').replace('\\u00a0', ' ')
        return item
