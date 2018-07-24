import scrapy


class DotamaxSpider(scrapy.Spider):
    name = 'dotamax'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']

    def parse(self, response):
        hero = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr::attr(onclick)').extract()
        hero_real_name = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td:nth-child(1) > span::text').extract()
        win_rate = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td > '
            'div.segment.segment-green::attr(style)').extract()
        for idx, h in enumerate(hero):
            url = h.replace('DoNav(\'', '').replace('\')', '')
            hero_name = url.replace('/hero/detail/', '')
            anti_url = '/hero/detail/match_up_anti/{}/'.format(hero_name)
            _wr = win_rate[idx].replace('width:', ''). \
                replace('%;', '')
            request = response.follow(anti_url, callback=self.parse_hero_anti)
            request.meta['hero_name'] = hero_name
            request.meta['hero_real_name'] = hero_real_name[idx]
            request.meta['win_rate'] = float(_wr)
            yield request

    def parse_hero_anti(self, response):
        hero_name = response.meta['hero_name']
        hero_real_name = response.meta['hero_real_name']
        win_rate = response.meta['win_rate']
        anti_index = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td:nth-child(2) > '
            'div:nth-child(1)::text').extract()
        anti_hero = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td:nth-child(1) > '
            'a::attr(href)').extract()
        anti = {}
        for idx, h in enumerate(anti_hero):
            anti_hero_name = h.replace('/hero/detail/', '')
            anti[anti_hero_name] = float(anti_index[idx].replace('%', ''))
        yield {
            'hero_name': hero_name,
            'hero_real_name': hero_real_name,
            'win_rate': win_rate,
            'anti': anti
        }
