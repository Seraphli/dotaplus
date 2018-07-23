import scrapy


class DotamaxSpider(scrapy.Spider):
    name = 'dotamax'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']

    def parse(self, response):
        resp = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr::attr(onclick)')
        win_rate = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td > '
            'div.segment.segment-green::attr(style)')
        for idx, r in enumerate(resp):
            url = r.extract().replace('DoNav(\'', '').replace('\')', '')
            hero_name = url.replace('/hero/detail/', '')
            _wr = win_rate[idx].extract().replace('width:', ''). \
                replace('%;', '')
            request = response.follow(url, callback=self.parse_hero)
            request.meta['hero_name'] = hero_name
            request.meta['win_rate'] = float(_wr)
            yield request
            if idx == 2:
                break

    def parse_hero(self, response):
        hero_name = response.meta['hero_name']
        win_rate = response.meta['win_rate']
        yield {
            'hero_name': hero_name,
            'win_rate': win_rate
        }
