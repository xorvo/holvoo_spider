import scrapy
import urlparse as parse
from holvoo_spider.items import Article


class ArticleSpider(scrapy.Spider):
    name = 'article'
    custom_settings = {
        'USER_AGENT': 'some value',
    }

    start_urls = [
        'http://www.holvoo.net/article/articleView.do?'
        'id=c00d7a11-4d0c-42d1-86fc-fada7875d994'
    ]

    def parse(self, response):
        article_id = self.id_from_url(response.url)
        content = response.css('div.ulag')
        title = content.css('h3::text').extract_first()
        subtitles = content.css('h6::text').extract()
        body = content.css('div.txt::text').extract()
        comments = response.css('div.lybox li.lybl_txt').extract()

        return Article({
            'id': article_id,
            'title': title,
            'subtitles': subtitles,
            'body': body,
            'comments': comments
        })

    @staticmethod
    def id_from_url(url):
        parsed = parse.urlsplit(url)
        query_dict = parse.parse_qs(parsed.query)
        return query_dict['id'][0]
