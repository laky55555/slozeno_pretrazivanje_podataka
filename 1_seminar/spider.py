import scrapy


class JutarnjiSpider(scrapy.Spider):
    name = 'JutarnjiSpider'
    allowed_domains = ['www.jutarnji.hr']
    start_urls = ['http://www.jutarnji.hr/']

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 10000
    }

    def parse(self, response):
        for article in response.css('.container > section'):

            # get article content
            content = '\n'.join(article.css('section#CImaincontent > div ::text').extract())
            content = '\n'.join(list(filter(None, content.splitlines())))

            if content == "":
                continue

            # get article tag list
            tags = []
            for t in article.css('.tags .list-inline ::text').extract():
                if t != '\n':
                    tags.append(t.replace('\n', ''))

            # yield article data
            yield {
                'title': article.css('h1.title ::text').extract_first(),
                'tags': tags,
                'content': content
                'url': response.url,
            }

        # get new batch of links to crawl
        next_pages = response.css('article a ::attr(href)').extract()
        for next_page in next_pages:
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
