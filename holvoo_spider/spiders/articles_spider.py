import scrapy
from math import ceil
from urllib import parse
from holvoo_spider.items import Article


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        'http://www.holvoo.net/index.do'
    ]

    def parse(self, response):
        channel_list_selector = 'ul.channellist li a::attr(href)'
        for channel in response.css(channel_list_selector).extract():
            yield response.follow(response.urljoin(channel),
                                  self.parse_channel)

    def parse_channel(self, response):
        # total article count and page size info is available in a script tag
        # we use the following xpath + regexp to get these data
        script_tags = response.xpath('//script/text()')
        exp = r'jpage\.init\(\'(\d+)\',\s\'(\d+)\'\)'
        total, page_size = list(map(int, script_tags.re(exp)))

        for pn in range(0, ceil(total / page_size)):
            list_url = '{url}&pn={pn}'.format(url=response.url, pn=pn)
            yield response.follow(list_url, self.parse_list)

    def parse_list(self, response):
        article_paths = response.css('div.list.mfont ul li span a::attr(href)').extract()
        for path in article_paths:
            article_url = response.urljoin(path)
            yield response.follow(article_url, self.parse_article)

    def parse_article(self, response):
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
